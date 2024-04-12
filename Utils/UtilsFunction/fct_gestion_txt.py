# -*- coding: utf-8 -*-

import numpy as np
import itertools
from tqdm import tqdm
import pandas as pd

def replace_all_tabs(path_in, path_out):
   ''' Replaces all tabs in a file with 4 spaces. Very useful to solve
   mixed usage of indents and space problems'''
   with open(path_in) as fin, open(path_out,'w') as fout:
      for line in fin:
          fout.write(line.replace('\t', '    '))

def readfile_normal(filepath):
    with open(filepath) as file:
        line = file.readline()
        return line

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
    """

    with open(filepath) as file:
        line_len = len(file.readline()[:-1].split(','))  # getting line lenght
        file.seek(0)  # go back to file start
        signal = np.zeros(line_len * n_lines, dtype=np.int16)  # reserve memory
        for i, line in enumerate(itertools.islice(file, n_skip, n_lines + n_skip)):
            try:
                ln = [int(i) for i in line[:-1].split(',')]  # read and convert line
                signal[i * line_len:(i + 1) * line_len] = ln  # put it in output
            except:
                pass
    return signal

def define_N_line(path):
    with open(path, "rbU") as f:
        num_lines = sum(1 for i in tqdm(f))

    return num_lines

def CountLastsZeros(x):
    """ Count number of elements up to the first non-zero element in reversed array, return that count """
    ctr = 0
    for i in range(1, x.size+1):
        k = x[-i]
        if k == 0:
            ctr += 1
        else: #short circuit evaluation, we found a non-zero so return immediately
            idx = - np.arange(i, x.size+1)
            return ctr, idx
    idx = - np.arange(i, x.size+1)
    return ctr, idx #we get here in the case that x was all zeros