# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 14:26:27 2023

@author: louis.combe
"""

import numpy as np 
import itertools

def readfile(filepath, n_skip, n_lines):
    """
    read signal data. filepath should be a folder such that data is
    stored in the following way:
        - filepath/signal.txt
            as a CSV formated file, with regular line lengths

    exec in O(n_skip * n_lines)
    memory consumption in O(n_lines)

    return:
        signal chunk (1D numpy array)
        ev_time (time series of *all* event times)
        ev_amp (time series of *all* event magnitudes (=log scale))
    """

    with open(filepath) as file:
        line_len = len(file.readline()[:-1].split(',')) # getting line lenght
        file.seek(0) # go back to file start
        signal = np.zeros(line_len*n_lines, dtype=np.int16) # reserve memory
        for i, line in enumerate(itertools.islice(file, n_skip, n_lines + n_skip)):
            try:
                ln = [int(i) for i in line[:-1].split(',')] # read and convert line
                signal[i*line_len:(i+1)*line_len] = ln # put it in output
            except:
                pass
    return signal
