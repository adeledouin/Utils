# -*- coding: utf-8 -*-
"""
Created on Tue May  7 16:59:49 2019
@author: Victor


USE CODEC FFV1 for uncompressed RGB videos !!




"""
import cv2
from skimage.color import rgb2gray
import numpy as np 
import matplotlib.pyplot as plt
from tqdm import tqdm
#from moviepy.editor import ImageSequenceClip
import imageio

def number_of_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    return cap.get(cv2.CAP_PROP_FRAME_COUNT)

def open_frame_n(video_path, frame_idx, channel = 'grey', get_fourcc = False):
    cap = cv2.VideoCapture(video_path)
    if get_fourcc:
        print(cap.get(cv2.CV_CAP_PROP_FOURCC))
    assert frame_idx < cap.get(cv2.CAP_PROP_FRAME_COUNT)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    _, frame = cap.read()
    if channel == 'grey':
        frame = rgb2gray(frame)
    elif isinstance(channel, int):
        frame = frame[:,:, channel]
    return frame
    

def open_multiple_frames(video_path, frame_list, channel = 'grey', open_all = False):
    Frames = []
    if open_all:
        frame_list = np.arange(int(number_of_frames(video_path)))
    for i in tqdm(frame_list):
        frame = open_frame_n(video_path, i, channel = channel)
        Frames.append(frame)
    Frames = np.array(Frames)
    return Frames

def video_to_image_folder(video_path, path_out,  frame_list, channel = 'grey'):
    for i in tqdm(frame_list):
        
        frame = open_frame_n(video_path, i, channel = channel)
        plt.imsave( path_out + str(i) + '.png', frame, cmap = 'gray')
        

# def frames_to_video(frames, pathOut, fps):
#     size = frames[0].shape
#     out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
#     for i,f in enumerate(frames):
#         out.write(f)
#     out.release()

def grayscale_to_fake_rgb(frame):
    return cv2.merge([frame, frame, frame])    

def create_gif(path_out, frames):
        imageio.mimsave(path_out, frames)
        
def frames_to_video(frames, path_out, fps = 1):
    size = (frames[0].shape[1], frames[0].shape[0])
    out = cv2.VideoWriter(path_out,cv2.VideoWriter_fourcc('F', 'F', 'V', '1'), fps, size)
    for i in range(len(frames)):
        # writing to a image array
        if frames[i].ndim < 3:
            img = grayscale_to_openCV(frames[i])
        else:
            img = frames[i]
        out.write(img)
    out.release()
    
    
def grayscale_to_openCV(img):
    img = img + np.abs(img.min())
    if img.max() != 0:
        img = (img / img.max()) * 255
    img = img.astype('uint8')
    img = np.dstack((img, img, img))
    return img

def video_to_video_diff(path_in, path_out):
    frames = open_multiple_frames(path_in,1, open_all=True)
    frames_diff = frames - frames[0]
    frames_to_video(frames_diff, path_out)
    
    
    
    