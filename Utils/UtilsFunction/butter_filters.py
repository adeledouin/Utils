# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:08:58 2021

@author: louis.combe
"""


import scipy.signal
import numpy as np


# ------------------------------------------
def low_pass_filter(signal, fc, acq_fr):
    # Application du filtre
    s_but = butter_filter(signal, fc, acq_fr, 'low')

    return s_but

# ------------------------------------------
def band_pass_filter(signal, fc, acq_fr):
    # Application du filtre
    s_but = butter_filter(signal, fc, acq_fr, 'band')

    return s_but

# ------------------------------------------
def butter(cutoff, fs, f_type, order=5):
    ''' Creates butter filter. f_type can be 'high' for highpass, 'low' for
    lowpass, 'band' for bandpass filter. If bandpass, cutoff must be an array of
    shape (2,)'''
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = scipy.signal.butter(order, normal_cutoff, btype=f_type, analog=False)
    return b, a


# ------------------------------------------
def butter_filter(data, cutoff, fs, f_type = 'low', order=5):
    ''' Applies butter filter to data. f_type can be 'high' for highpass,
    'low' for lowpass, 'band' for bandpass filter.
    If bandpass, cutoff must be an array of  shape (2,)'''
    if f_type == 'bandstop':
        assert len(cutoff) == 2, 'Cutoff must be of len 2 for bandpass'
        if type(cutoff) != np.ndarray:
            cutoff = np.array(cutoff)
    b, a = butter(cutoff, fs, f_type=f_type, order=order)
    y = scipy.signal.filtfilt(b, a, data)
    return y

def butter_highpass_filter(data, lowcut, fs, order=5):
    """Apply a high-pass Butterworth filter to the input data.

    Parameters:
    data (numpy array): Input data to be filtered.
    lowcut (float): Cutoff frequency (Hz) for the high-pass filter.
    fs (float): Sampling frequency (Hz) of the input data.
    order (int): Order of the Butterworth filter. Default is 5.

    Returns:
    numpy array: Filtered data.
    """
    nyq = 0.5 * fs
    high = lowcut / nyq
    b, a = butter(order, high, btype='highpass')
    y = scipy.signal.filtfilt(b, a, data)
    return y
