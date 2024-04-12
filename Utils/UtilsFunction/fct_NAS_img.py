# -*- coding: utf-8 -*-
import subprocess

# %% imports

import numpy as np
from subprocess import call, check_output
import shlex
import logging

from Utils.Module.fct_path import create_directory_if_not_exists
from Utils.Module.fct_verbose import printv
import os
from matplotlib.pyplot import imread



def get_panorama(idx, NAS_client, NAS_path, save_path, to_look_img):
    id_img = to_look_img[idx]
    printv('Fetching panorama for pict {}'.format(to_look_img))

    create_directory_if_not_exists(save_path)

    cmd = 'scp -i ~/.ssh/id_rsa {}:{}{}.png {}.png'.format(NAS_client, NAS_path, id_img,
                                                           '{}{}'.format(save_path,
                                                               id_img))
    try:
        out = call(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


def get_single_cam_img(i, NAS_client, NAS_path, fnl, cam_id, tmp_dir, pic_id):
    ext = '_yuv_dyclop{}'.format(cam_id)
    pic_name = str(int(fnl[pic_id[i]])) + ext
    logging.debug('recup {} from NAS'.format(pic_id[i]))
    cmd = 'rsync -av --progress {}:{}{}c/{} {}{}_{}'.format(NAS_client, NAS_path, cam_id, pic_name,
                                                            tmp_dir.format(cam_id), pic_id[i], cam_id)
    logging.debug('run cmd : {}'.format(cmd))
    try:
        out = check_output(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

def count_nb_pict(NAS_client, NAS_path, cam_id):
    logging.debug('count {}c from NAS'.format(cam_id))
    cmd = 'cd {}:{}{}c/'.format(NAS_client, NAS_path, cam_id)
    cmd_count = 'ls | wc -l'
    logging.debug('run cmd : {}'.format(cmd))
    try:
        out = check_output(shlex.split(cmd))
        out = check_output(shlex.split(cmd_count))
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))

def transfert_single_cam_img(pic_id, ssh_client, ssh_path, cam_id, tmp_dir):
    pic_name = '{}_{}'.format(pic_id, cam_id)
    cmd = 'rsync -av {}:{}{}c/tmp/{} {}{}'.format(ssh_client, ssh_path, cam_id, pic_name, tmp_dir, pic_name)
    try:
        out = check_output(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


def get_FNL_file(NAS_client, NAS_path, cam_id, FNL_name, save_path):
    cmd = 'rsync -av --progress {}:{}{}c/{} {}{}'.format(NAS_client, NAS_path, cam_id, FNL_name, save_path, FNL_name)
    logging.info('execute {}'.format(cmd))
    try:
        out = check_output(shlex.split(cmd))
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))


def get_images(NAS_client, NAS_path, tmp_dir ,pic_id, all_FNL, camlist): # for the moment only explicit args, bc i dont know how the final code will be organised
    ''' Transfer images for a given timestamp (pic_id) from the NAS to a tmp directory one the local system,
for each camera'''

    printv('Fetching images for pic {}'.format(pic_id))
    for i, cam_id in enumerate(camlist):
        fnl = all_FNL[cam_id] # fnl: file name list, fnl[i] outputs name of file corresponding to timestamp i
        out = get_single_cam_img(i, NAS_client, NAS_path, fnl, cam_id, tmp_dir, pic_id)


def clean_tmp(tmp_dir, pic_id):
    printv('Cleaning for timestamp: {}'.format(pic_id))
    cmd = 'rm {}{}_*'.format(tmp_dir, pic_id)
    os.system(cmd)

def load_single_imge(path, pic_id, cam_id, flip):
    '''
    Function dedicated to load images stored in tmp directory after
    fetching from NAS
    '''

    path_i = path + '{}_{}'.format(pic_id, cam_id)
    image = read_images(path_i, flip)
    return image


def load_images(path, pic_id, cam_ids, flips):
    '''
    Function dedicated to load images stored in tmp directory after
    fetching from NAS
    '''

    images = [0 for i in range(cam_ids.size)]
    for i in cam_ids:
        logging.debug('path = {}'.format(path.format(i)))
        images[i] = (load_single_imge(path.format(i), pic_id, i, flips[i]))
    return images


def read_images(path, flip=0):
    """ read images and return them as R/G/B channel list """
    try:
        image = OpenImage(path)
    except:
        image = imread(path)
    # rotate is needed
    if image.shape[1] > image.shape[0]:
        image = image.swapaxes(0, 1)
    if flip:
        image = np.flipud(image)
        image = np.fliplr(image)
    # return R G B channels
    return image


def OpenImage(filepath, width=4036, height=1340):
    """ from http://picamera.readthedocs.io/en/release-1.12/recipes2.html """

    stream = open(filepath, 'r')
    # Rewind the stream for reading
    stream.seek(0)
    # Calculate the actual image size in the stream (accounting for rounding
    # of the resolution)
    fwidth = (width + 31) // 32 * 32
    fheight = (height + 15) // 16 * 16
    L = fwidth * fheight
    # Load the Y (luminance) data from the stream
    data = np.fromfile(stream, dtype=np.uint8)

    Y = data[:L].reshape((fheight, fwidth))

    U = data[L:int(L * 1.25)].reshape(fheight // 2, fwidth // 2)
    U = U.repeat(2, axis=0).repeat(2, axis=1)

    V = data[int(L * 1.25):].reshape(fheight // 2, fwidth // 2)
    V = V.repeat(2, axis=0).repeat(2, axis=1)

    # Stack the YUV channels together, crop the actual resolution, convert to
    # floating point for later calculations, and apply the standard biases

    YUV = np.dstack((Y, U, V))[:height, :width, :].astype(np.float64)
    YUV[:, :, 0] = YUV[:, :, 0] - 16  # Offset Y by 16
    YUV[:, :, 1:] = YUV[:, :, 1:] - 128  # Offset UV by 128
    # YUV conversion matrix from ITU-R BT.601 version (SDTV)
    #              Y       U       V
    M = np.array([[1.164, 0.000, 1.596],  # R
                  [1.164, -0.392, -0.813],  # G
                  [1.164, 2.017, 0.000]])  # B
    # Take the dot product with the matrix to produce RGB output, clamp the
    # results to byte range and convert to bytes
    RGB = YUV.dot(M.T).clip(0, 255).astype(np.uint8)
    stream.close()

    return RGB
