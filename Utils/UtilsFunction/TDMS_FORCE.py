# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 11:32:54 2021

@author: manip-liquides
"""

from nptdms import TdmsFile
import numpy as np
from matplotlib import pyplot as plt


def open_tdms(path):
    """ Open the tdms file and store each of the 6 signals in a dictionnary. """
    file = TdmsFile(path)
    a = file.as_dataframe()
    signals = {}
    signals[0] = np.array(a[a.columns[0]])
    signals[1] = np.array(a[a.columns[1]])
    # signals[2] = np.array(a[a.columns[2]])
    # signals[3] = np.array(a[a.columns[3]])
    # signals[4] = np.array(a[a.columns[4]])
    # signals[5] = np.array(a[a.columns[5]])
    # signals[6] = np.array(a[a.columns[6]])
    # signals[7] = np.array(a[a.columns[7]])

    plt.plot(signals[0][::10], '-b')
    plt.plot(signals[1][::10], '-r')
    # plt.plot(signals[2][::10],'-g')
    # plt.plot(signals[3][::10],'-k')
    # plt.plot(signals[4][::10],'-c')
    # plt.plot(signals[5][::10],'-m')
    # plt.plot(signals[6][::10],'-y')
    # plt.plot(signals[7][::10],'-k')

    # for k in range(8):
    #     #plt.plot(signals[k][::50]+15000*k)
    #     plt.plot(signals[k][::10])
    #     #plt.plot(signals[k])

    plt.show()
    return signals