# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:15:53 2019

@author: Victor
"""

import numpy as np
from time import time

import matplotlib.pyplot as plt
from matplotlib import cm

from skimage.filters import scharr
from skimage.feature import canny

from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.filters import minimum_filter, maximum_filter
from skimage.feature import peak_local_max
from scipy.signal import convolve2d, correlate2d
from skimage.transform import hough_circle
from skimage.morphology import erosion, dilation
import cv2 as cv


#########################################################################################################
# Strain extraction

# a) Force evaluation from luminosity profile
#########################################################################################################

def force_pixelvalues(box, mask):
    return box[mask == 1]


def force_G2(box, mask, pixel_size=1, **kwargs):
    """ return the gradient square of box and applies mask
    to it."""

    # rolls in every direction to prepare for grandient computation
    ip, im = np.roll(box, 1, 0), np.roll(box, -1, 0)
    jp, jm = np.roll(box, 1, 1), np.roll(box, -1, 1)
    pp, mm = np.roll(ip, 1, 1), np.roll(im, -1, 1)
    pm, mp = np.roll(ip, -1, 1), np.roll(im, 1, 1)

    # computes gradient in every direction
    A = (im - ip) / (2 * pixel_size)
    B = (jm - jp) / (2 * pixel_size)
    C = (mm - pp) / (pixel_size * 2 * np.sqrt(2))
    D = (pm - mp) / (pixel_size * 2 * np.sqrt(2))

    # sums the square of the gradient to compute G squared
    out = (A ** 2 + B ** 2 + C ** 2 + D ** 2) / 4
    return np.sum(out * mask) / np.sum(mask)


def force_lum(box, mask, **kwargs):
    """ return mean of values over median, (not) normalized by median"""
    data = (box * mask).flatten()
    data = data[data != 0]
    return np.mean(data[data > np.percentile(data, 90)] / np.percentile(data, 90))


##################################################################################

# b) Helpers for geometry and masks cration

##################################################################################

def circle_zone(r, rext=0):
    """
    return a binary square image, with a circle=1 inside, of radius r.
    The circles touches the edges of the picture.
    """
    if rext == 0:
        rext = r
    out = np.zeros([2 * rext - 1, 2 * rext - 1])
    for i in range(2 * rext - 1):
        for j in range(2 * rext - 1):
            if (i - rext + 1) ** 2 + (j - rext + 1) ** 2 <= r ** 2:
                out[i, j] = 1
    return out


def find_contact_from_centers(coordA, coordB, ratio=0.7):
    '''
    Returns the point halfway between two points on a 2D image.
    Is used to find localisation of a contact when two bead centers are given.

    ratio: use this to return a point only ratio * halfway instead of halfway
    from coordA
    '''

    xa, ya = coordA
    xb, yb = coordB

    xc = xa + ((xb - xa) * ratio) / 2
    yc = ya + ((yb - ya) * ratio) / 2
    return int(xc), int(yc)


def extract_square(x, y, r, image):
    '''
    Creates a box of size 2*r, centered around (x,y), and a circular mask of
    radius r centered on (x,y)
    '''
    box = image[x - r:x + r - 1, y - r:y + r - 1]
    mask = circle_zone(r)
    return box, mask


def extract_rect(coordA, coordB, image, thickness=8):
    '''
    Creates a mask from coordA to coordB, with a thickness set by 'thickness'. The image is cropped
    to a box that contains the mask.
    '''

    xA, yA = coordA
    xB, yB = coordB

    # Mask creation
    mask = np.zeros((image.shape[0], image.shape[1], 3))
    mask = cv.line(mask, (xA, yA), (xB, yB), color=(1, 1, 1), thickness=thickness)
    mask = mask[:, :, 0]

    # Define the limitations of the box
    xlow, xhigh = min(xA, xB) - thickness // 2, max(xA, xB) + thickness // 2
    ylow, yhigh = min(yA, yB) - thickness // 2, max(yA, yB) + thickness // 2

    xlow, ylow = max(0, xlow), max(0, ylow)
    box, mask = image[ylow:yhigh, xlow:xhigh], mask[ylow:yhigh, xlow:xhigh]
    return box * 1., mask * 1.


####################################################################################

# c) main strain evaluation functions

####################################################################################


def eval_strain(image, c, r, method, pixel_size=1):
    """ evaluate (sort of) the strain in the grain """
    s = []
    for i, (x, y) in enumerate(c):
        box, mask = extract_square(x, y, r[i], image)
        s += [method(box, mask, pixel_size=pixel_size)]
        if i == -1:
            plt.imshow(box)
            plt.figure()
            plt.imshow(box * mask)
    return s


def eval_strain_contacts(img, grain_in_contact, x, y, method=force_G2,
                         thresh_no_contact=100, pixel_size=1, thickness=15, ratio=0.7):
    '''
    Main function for the computation of strain around the contacts.

    PARAMETERS

    img: image to be analysed

    grain_in_contact: list of contacts. In the format [[0,2], [0,178], [1,12], ...]
    with no repetion, i.e if [0,2] is in the list, [2,0] will not be. This format matches
    the format outputed by network.grain_in_contact

    c: list of centers [[x0, x1, x2...], [y0, y1, y2...]]

    method: function used for the computation of the strain on the masked image

    thresh_no_contact: threshold for contact removal. If min(box * mask) < thresh_no_contact
    then the contact is set to have a strain of zero.

    pixel_size: size of a pixel in the real space, in meter/pixel

    thickness: thickness of the mask around the contact

    ratio: pourcentage of the radius of the bead to keep for the analysis, in order
    to avoid including the border of the bead in the contact (gradient very sensitive
    to the inclusion of borders)
    '''

    s = []
    y, x = x, y  # I fucked up somewhere but i dont really know where. Works like this
    for g in grain_in_contact:
        i, j = g
        xa, xb = x[i], x[j]
        ya, yb = y[i], y[j]

        # start by finding the contact, halfway between the beads centers

        xc, yc = find_contact_from_centers((xa, ya), (xb, yb), ratio=ratio)
        # box and mask extraction
        box, mask = extract_rect((xc, yc), (xa, ya), img, thickness=thickness)
        im = box * mask
        m = im[im > 0].min()
        if m < thresh_no_contact:  # remove contact if lum falls too low
            G2 = 0
        else:  # if not, compute G2 with the method
            G2 = method(box, mask, pixel_size=pixel_size)
        G2_1 = G2

        # Contact is symmetrical, and we analyse only one side, so we switch
        # i,j to j,i, and redo the analysis.
        j, i = g
        xa, xb = x[i], x[j]
        ya, yb = y[i], y[j]
        xc, yc = find_contact_from_centers((xa, ya), (xb, yb), ratio=ratio)
        box, mask = extract_rect((xc, yc), (xa, ya), img, thickness=thickness)
        im = box * mask
        m = im[im > 0].min()
        if m < thresh_no_contact:
            G2 = 0
        else:
            G2 = method(box, mask, pixel_size=pixel_size)
        G2_2 = G2

        if G2_1 == 0 or G2_2 == 0:
            s.append(0)
        else:
            s.append(np.mean([G2_1, G2_2]))
    return s


#########################################################################################################
# Find box and sensors
#########################################################################################################

def find_box_and_sensors(image, C, R):
    bati, sensor = input_data(image)

    bati_left, bati_top, bati_right, bati_bottom = bati[:2], bati[2:4], bati[4:6], bati[6:]

    touching_left = find_touching_grains(bati_left, C, R)
    touching_top = find_touching_grains(bati_top, C, R)
    touching_right = find_touching_grains(bati_right, C, R)
    touching_bottom = find_touching_grains(bati_bottom, C, R)

    touching = [touching_left, touching_top, touching_right, touching_bottom]

    x_capt = sensor[:, 0].reshape([3, 2])
    y_capt = sensor[:, 1].reshape([3, 2])

    x_cont, y_cont = [], []
    x_cont += [C[touching_left, 0]]
    y_cont += [C[touching_left, 1] - R[touching_left]]
    x_cont += [C[touching_top, 0] - R[touching_top]]
    y_cont += [C[touching_top, 1]]
    x_cont += [C[touching_right, 0]]
    y_cont += [C[touching_right, 1] + R[touching_right]]
    x_cont += [C[touching_bottom, 0] + R[touching_bottom]]
    y_cont += [C[touching_bottom, 1]]

    return x_capt, y_capt, x_cont, y_cont, touching, bati


def find_touching(xc, yc, C):
    xc, yc = xc.flatten(), yc.flatten()
    touching = np.zeros([len(xc), 4])
    for i, (xcc, ycc) in enumerate(zip(xc, yc)):
        d2 = (xcc - C[:, 0]) ** 2 + (ycc - C[:, 1]) ** 2
        touching[i] = d2.argsort()[:4]
    return touching


def input_data(image):
    lx, ly, _ = image.shape
    bati = []
    sensors = []
    FIGSIZE = (10, 10)
    fig, ax = plt.subplots(figsize=FIGSIZE)
    img = np.mean(image, -1)

    ax.imshow(img[lx // 2:, :ly // 2]);
    ax.set_title('1 - Click on lower left frame border')
    bati += plt.ginput(1)
    plt.close(fig);
    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.imshow(img[:lx // 2, :ly // 2]);
    ax.set_title('2 - Click on higher left frame border')
    bati += plt.ginput(1)
    plt.close(fig);
    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.imshow(img[:lx // 2, :ly // 2]);
    ax.set_title('3 - Click on left top frame border')
    bati += plt.ginput(1)
    plt.close(fig);
    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.imshow(img[:lx // 2, ly // 2:]);
    ax.set_title('4 - Click on right top frame border')
    bati += plt.ginput(1)
    plt.close(fig);
    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.imshow(img[:lx // 2, ly // 2:]);
    ax.set_title('5 - Click on higher right frame border')
    bati += plt.ginput(1)
    plt.close(fig);
    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.imshow(img[lx // 2:, ly // 2:]);
    ax.set_title('6 - Click on lower right frame border')
    bati += plt.ginput(1)
    plt.close(fig);
    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.imshow(img[lx // 2:, :ly // 2]);
    ax.set_title('7 - Click on left bottom frame border')
    bati += plt.ginput(1)
    plt.close(fig);
    fig, ax = plt.subplots(figsize=FIGSIZE)

    ax.imshow(img[lx // 2:, ly // 2:]);
    ax.set_title('8 - Click on right bottom frame border')
    bati += plt.ginput(1)
    plt.close(fig);
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.imshow(img);
    ax.set_title('9 - Click on all six sensors tip')
    sensors += plt.ginput(6)
    plt.close(fig)

    bati = np.array(bati)
    shift = np.zeros_like(bati)
    shift[:, 1] = [lx // 2, 0, 0, 0, 0, lx // 2, lx // 2, lx // 2]
    shift[:, 0] = [0, 0, 0, ly // 2, ly // 2, ly // 2, 0, ly // 2]

    return np.fliplr(bati + shift), np.fliplr(np.array(sensors))


def find_touching_grains(border, centers, radii):
    touching = []
    for i, (center, radius) in enumerate(zip(centers, radii)):
        dist = point_2_line(center, border)
        if dist < 1.1 * radius:
            touching += [i]
    return touching


def point_2_line(point, line_points):
    (xa, ya), (xb, yb) = line_points
    x, y = point
    nom = np.abs((yb - ya) * x - (xb - xa) * y - xa * yb + xb * ya)
    denom = np.sqrt((yb - ya) ** 2 + (xb - xa) ** 2)
    return nom / denom


# DUMP BELOW
################################################################################
################################################################################
################################################################################

def threshold_image(image, r_smooth=5):
    """ threshold the grain image (sort of) without the force chains """
    # R = image[:,:,0] ; G = image[:,:,1] ; B = image[:,:,2]
    # return canny(image.min(-1), r_smooth)
    return canny(image[:, :, 2], r_smooth)


def force_slope(box, mask, frac=0.95):
    data = (box * mask).flatten()
    data = data[data != 0]
    data.sort();
    L = len(data)
    y1 = data[-1];
    y0 = data[int(frac * L)]
    x1 = L;
    x0 = int(frac * L)
    return (y0 - y1) / (x1 - x0)


def force_delta(box, mask, full=False):
    """ return luminosity high-low delta """
    data = (box * mask).flatten()
    data = data[data != 0]
    low, high = np.percentile(data, 50), np.percentile(data, 97)
    L, H = np.mean(data[data <= low]), np.mean(data[data >= high])
    if full:
        return H - L, data
    else:
        return H - L


def force_ratio(box, mask):
    """ return luminosity high-low ratio """
    data = (box * mask).flatten()
    data = data[data != 0]
    low, high = np.percentile(data, 10), np.percentile(data, 90)
    L, H = np.mean(data[data <= low]), np.mean(data[data >= high])
    return H / L
