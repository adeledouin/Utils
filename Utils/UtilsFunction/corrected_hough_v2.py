import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
from scipy import ndimage


# from adaptative_thresholding import threshold_local

def remove_low_lum(img, x_circles, y_circles, R_circles=None, R_filter=10, lum_min_remove=50, **kwargs):
    '''Removes the false positives after hough circle detection.  Checks the
    median luminosity around the centers detected by HoughCircles.
    -------
    img: base img
    x_circles, y_circles: coordinates of the centers
    R_filter: length of the square on which the luminosity is checked
    lum_min_remove: threshold for beads removal. If median(lum) < lum_min_remove,
    the bead is removed
    '''

    to_remove = []
    for i in range(len(x_circles)):
        xc, yc = int(x_circles[i]), int(y_circles[i])  # no need to worry about ceil or floor, 0.5 pixel is no big deal
        xl, xh, yl, yh = max(0, xc - R_filter), max(0, xc + R_filter), max(0, yc - R_filter), max(0, yc + R_filter)
        to_check = img[yl:yh, xl:xh].flatten()
        lum_circ = np.median(to_check)
        if lum_circ < lum_min_remove:  # if the lumi is to low, delete
            to_remove += [i]
    if type(R_circles) == type(None):
        return np.delete(x_circles, to_remove), np.delete(y_circles, to_remove)
    else:
        return np.delete(x_circles, to_remove), np.delete(y_circles, to_remove), np.delete(R_circles, to_remove)


def corrected_hough(img, h_param1=100, h_param2=1, min_dist=45, min_rad=22, max_rad=30,
                    correct=True, radii=False, **kwargs):
    '''OPENCV's HoughCircles transform with correction. By default, only removes false
    positives based on luminosity tests. More advanced features (filling) are
    available in corrected_hough and filter_and_fill modules, and might be implemented here in the future.
    ----

     '''

    if len(img.shape) > 2:
        img = img[:, :, 1]

    # Perform houghcircle detection
    hough = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, min_dist,
                             param1=h_param1, param2=h_param2, minRadius=min_rad,
                             maxRadius=max_rad)

    circles = hough[0]
    x_circles = circles[:, 0]
    y_circles = circles[:, 1]
    R_circles = circles[:, 2]

    # Output without correction if wanted
    if correct == False:
        if radii:  # To output the circles radii
            return x_circles, y_circles, R_circles
        else:
            return x_circles, y_circles
    if correct:  # Output with correction. (radii not implemented yet)
        if radii:
            x_f, y_f, R_f = remove_low_lum(img, x_circles,
                                           y_circles, R_circles=R_circles, **kwargs)
            return x_f, y_f, R_f
        else:
            x_f, y_f = remove_low_lum(img, x_circles, y_circles, **kwargs)
        return x_f, y_f

# def corrected_hough_with_flattening(raw, crop = [80,1670], remove_high_lum_crown = [125, 150],
# block_size = 101 ,  offset = 100, h_param1 = 100, lum_min_remove = 65, radii = True):
#
#    raw = np.array(raw, dtype = np.uint8())
#    crop1,crop2 = crop
#    img = raw[crop1:crop2,:,2]
#    boundary_high_lum_crown = remove_high_lum_crown[0] - crop1
#    threshold_high_lum_crown = remove_high_lum_crown[1]
#    img[:boundary_high_lum_crown][img[:boundary_high_lum_crown] > threshold_high_lum_crown] = 0
#    
#    
#    thr = threshold_local(img, block_size, method='mean', offset=offset)
#    
#    img = img - thr
#    img = np.maximum(img, np.zeros_like(img))
#    img = img.astype('uint8')
#    x,y, R = corrected_hough(img, h_param1 = h_param1, lum_min_remove= lum_min_remove, radii = True)
#    y = y + crop1
#    if radii:
#        return x, y, R
#    else:
#        return x,y
