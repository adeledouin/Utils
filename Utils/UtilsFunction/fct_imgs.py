
import numpy as np
import imageio
from matplotlib import pyplot as plt
import cv2 as cv

from Utils.Package.panostitching.classStitcher import Stitcher
import logging


def binary_thresh_img(img, seuil, condition):
    binary = np.zeros(img.shape, dtype=np.int8)
    if condition == 'suppequal':
        where = np.where(img >= seuil)
    elif condition == 'supp':
        where = np.where(img > seuil)
    elif condition == 'infequal':
        where = np.where(img <= seuil)
    elif condition == 'inf':
        where = np.where(img < seuil)
    else:
        where = np.where(img == seuil)

    binary[where] = 255
    return binary


def clustering(binary, min_area):
    retval, labels, stats, centroids = cv.connectedComponentsWithStats(binary, connectivity=8)

    to_keep_labels = np.where(stats[:, -1] > min_area)[0]
    to_unkeep_labels = np.where(stats[:, -1] <= min_area)[0]

    for l, label in enumerate(to_unkeep_labels):
        where = np.where(labels == label)
        labels[where] = 0
    for l, label in enumerate(to_keep_labels):
        where = np.where(labels == label)
        labels[where] = l

    stats = stats[to_keep_labels, :]
    centroids = centroids[to_keep_labels, :]

    return to_unkeep_labels.size, labels, stats, centroids


def find_center_col(center_index, stats):

    # Calculer la distance de chaque élément par rapport au centre
    distances_to_center = np.abs(stats[:, 0] - center_index)

    # Trouver l'index de la valeur la plus proche du centre
    closest_index = np.argmin(distances_to_center)

    # Obtenir la valeur la plus proche du centre
    x = stats[closest_index, 0]
    range = stats[closest_index, 2]
    area = stats[closest_index, -1]

    return x, range, area


def is_bad_lum(retval, nb_cluster):
    if retval > nb_cluster:
        bad_lum = True
    else:
        bad_lum = False

    return bad_lum


def shift_image_yaxis(image, dy):
    ''' Shifts an image on the y axis. All images should be cropped by the max diff (to avoid zero padded area)'''
    canvas = np.zeros_like(image)
    height = image.shape[0]
    if dy == 0:
        return image
    elif dy > 0:
        canvas[dy:] = image[:-dy]
    elif dy < 0:
        canvas[:dy] = image[-dy:]
    return canvas


def sum_pxl(img):
    where_channel = np.size(img.shape) - 1
    return np.sum(img, axis=where_channel)


def zoom_img(img, ini=0, end=1000, col=None, channel=None):
    if col is not None and channel is not None:
        return img[ini:end, col, channel]
    elif col is not None:
        return img[ini:end, col, :]
    elif channel is not None:
        return img[ini:end, :, channel]
    else:
        return img[ini:end, :, :]


def where_seq(to_look, pic_ids):
    return np.where(to_look == pic_ids)[0][0]


def find_line(img, column):
    lines_for_mean = []
    lines_for_sigma = np.array([])

    for i in column:
        where_min_sum = np.where((sum_pxl(img[:, i, :]) == np.min(
            sum_pxl(zoom_img(img, col=i)))
                                  ) & (sum_pxl(img[:, i, :]) < 50
                                       ))[0]
        if where_min_sum.size == 0:
            logging.debug('colone {} {}'.format(i, where_min_sum.size))
            lines_for_mean.append(np.nan)
        else:
            logging.debug('line trouvée {} {}'.format(i, where_min_sum.size))
            lines_for_mean.append(where_min_sum[0])
        where_pxs_lin = np.where(sum_pxl(zoom_img(img, col=i)) < 50)[0]
        lines_for_sigma = np.concatenate((lines_for_sigma, where_pxs_lin))

    return lines_for_mean, lines_for_sigma, column



def diff_channel(ini, end):
    return np.int8(end) - np.int8(ini)


def diff_img(ini, end):
    diff = np.zeros((ini.shape[0], ini.shape[1], ini.shape[2]), dtype=np.int8)
    for channel in range(3):
        diff[:, :, channel] = end[:, :, channel] - ini[:, :, channel]

    return diff


def diff_seq_cam(seq, delta_img=1):
    diff = np.zeros((seq.shape[0] - delta_img, seq.shape[1], seq.shape[2], seq.shape[3]), dtype=np.int8)
    for p, pic in enumerate(range(seq.shape[0] - delta_img)):
        diff[p, :, :, :] = diff_img(seq[p, :, :, :], seq[p + delta_img, :, :, :])
    return diff


def diff_seq(seq, cam_ids, delta_img=1):
    diff = [0 for c in np.arange(cam_ids.size)]
    for c, cam in enumerate(cam_ids):
        logging.debug(f"c = {c}")
        diff[c] = diff_seq_cam(seq[c], delta_img)
    return diff


def scalar_diff_channel(diff, methode = 'sum'):
    if methode == 'sum':
        return np.sum(np.abs(diff))

def scalar_diff_img(diff, methode = 'sum'):
    scalar = np.zeros(diff.shape[-1])
    for channel in range(3):
        scalar[channel] = scalar_diff_channel(diff[:, :, channel], methode)

    return scalar

def scalar_diff_seq_cam(seq_diff, methode = 'sum'):
    scalar = np.zeros((seq_diff.shape[0], seq_diff.shape[3]))
    for p, pic in enumerate(range(seq_diff.shape[0])):
        scalar[p, :] = scalar_diff_img(seq_diff[p, :, :, :], methode)
    return scalar


def scalar_diff_seq(seq_diff, cam_ids, methode = 'sum'):
    scalar = [0 for c in np.arange(cam_ids.size)]
    for c, cam in enumerate(cam_ids):
        logging.debug(f"c = {c}")
        scalar[c] = scalar_diff_seq_cam(seq_diff[c], methode)
    return scalar


def recup_FNL_name(fnl, pic_id):
    pic_name = str(int(fnl[pic_id]))
    return pic_name


def compare_name(name, name_p):
    if name_p == name:
        same = 1
    else:
        same = 0
    return same


def is_missing_img_cam(pic_ids, fnl):
    logging.debug(f"pic_ids = {pic_ids}")
    same_name = np.zeros(pic_ids.size)
    name = 'bla'
    for p, pic in enumerate(pic_ids):
        name_p = recup_FNL_name(fnl, pic_id=pic)
        same_name[p] = compare_name(name, name_p)
        name = name_p
    return same_name


def is_missing_img(pict, pic_ids, cam_ids):
    missing = [0 for c in np.arange(cam_ids.size)]
    for c, cam in enumerate(cam_ids):
        logging.debug(f"c = {c}")
        missing[c] = is_missing_img_cam(pic_ids, pict.campict[c].fnl)
    return missing


def compare_tps(t_evnt, t_pic, lag=0.2):
    if np.abs(t_evnt - t_pic) > lag:
        overlap = 0
    else:
        overlap = 1
    return overlap


def is_in_overlap(t_events, t_pics, lag=0.2):
    logging.info(f"{np.zeros(t_events.size)}")
    in_overlap = np.zeros(t_events.size)
    for e, t_event in enumerate(t_events):
        logging.info(f"{e} {t_event} {t_pics[e]}")
        in_overlap[e] = compare_tps(t_event, t_pics[e], lag=lag)
    return in_overlap

def find_shift_yaxis(images, plot = False,  ratio=0.75, reprojThresh=4.0):
    '''
    Find the shifts between cameras by computing their key features, matching
    them by pair. For each pair, the shift is computed and the image shift is
    defined as the median of these shifts.

    PARAMETERS---------------------------------------------------------------

    images = list of images to be preprocessed
    plot:
    Boolean. If True, plots the shifts
    '''

    stitcher = Stitcher()

    med_diff = []

    for i in range(len(images) - 1):
        imageA = images[i]
        imageB = images[i + 1]
        (kpsB, featuresB) = stitcher.detectAndDescribe(imageB)
        (kpsA, featuresA) = stitcher.detectAndDescribe(imageA)

        M = stitcher.matchKeypoints(kpsA, kpsB,
            featuresA, featuresB, ratio, reprojThresh)

        (matches, H, status) = M

        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]

        matches_localisation = []

        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully
            # matched
            if s == 1:
                # draw the match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                matches_localisation.append([ptA, ptB])
        matches_localisation = np.array(matches_localisation)
        loc_y = matches_localisation[:,:,1]
        if plot:
            plt.plot(np.diff(loc_y), label = str(i) + ' : ' + str(np.median(np.diff(loc_y))))
        med_diff.append(np.median(np.diff(loc_y)))
    if plot:
        plt.ylim(-15,15)
        plt.legend()
    med_diff = -np.array(med_diff)
    consecutive_diffs = [np.sum(med_diff[:i]) for i in range(1, len(med_diff) + 1)]
    consecutive_diffs.insert(0,0)
    return consecutive_diffs
