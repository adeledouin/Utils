# -*- coding: utf-8 -*-

import numpy as np
from numpy.fft import fft, fftfreq

# ------------------------------------------
def fourier_transform(signal, fr):
    f_k = fft(signal)  # Transformée de fourier
    f_k_abs = np.absolute(f_k)

    freq = fftfreq(signal.size, d=1 / fr)  # Fréquences de la transformée de Fourier

    return freq, f_k_abs

# ------------------------------------------
def my_histo(y: np.ndarray, min_val: int, max_val: int, x_axis: str, y_axis: str, density,
             binwidth, nbbin, hybridbin=None) -> tuple:
    """
    Compute a histogram of the input data `y`.
    :param y: array-like input data to do histo.
    :param min_val: minimum value of the histogram range.
    :param max_val: maximum value of the histogram range.
    :param x_axis: the type of the x-axis, 'lin' or 'log'.
    :param y_axis: the type of the y-axis, 'lin' or 'log'.
    :param density: whether to normalize the histogram, 0 for no normalization, 1 for density, and 2 for probability.
    :param binwidth: the width of the bins. If `nbbin` is provided, `binwidth` is ignored.
    :param nbbin: the number of bins to use. If `hybridbin` is provided, `nbbin` is ignored.
    :param hybridbin: an array of bin edges. If provided, `nbbin` and `binwidth` are ignored.
    :return: a tuple containing the histogram values and the bin centers.
    :raises ValueError: if `binwidth` is not None and `nbbin` is None.
    """
    if min_val is None:
        min_val = np.min(y)

    if max_val is None:
        max_val = np.max(y)

    if nbbin is None and binwidth is None:
        bin_edges = hybridbin
        count, _ = np.histogram(y, bins=bin_edges, density=False)

    elif nbbin is None:
        bin_edges = np.arange(min_val, max_val + binwidth, binwidth)
        count, _ = np.histogram(y, bins=bin_edges, density=False)

    elif binwidth is None:
        if x_axis == 'lin':
            binwidth = (max_val - min_val) / nbbin
            bin_edges = np.arange(min_val, max_val + binwidth, binwidth)
        else:
            bin_edges = np.logspace(np.log10(min_val), np.log10(max_val), nbbin)

        count, _ = np.histogram(y, bins=bin_edges, density=False)
    else:
        raise ValueError('Bin edges are not defined.')

    if density == 0:
        hist = count
    elif density == 1:
        hist = count / np.diff(bin_edges)
    else:
        hist = count / np.diff(bin_edges) / np.sum(count)

    x_axis_array = bin_edges[:-1] + np.diff(bin_edges) / 2

    return hist, x_axis_array
