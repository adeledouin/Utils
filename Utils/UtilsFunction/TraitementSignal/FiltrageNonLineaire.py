#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 17:17:02 2023

@author: sroux
"""

# import libraries
import numpy as np
import scipy
import matplotlib.pyplot as plt


# from pypher.pypher import psf2otf


# %%
def prox_L1(wx, gamma):
    wp = np.maximum(np.abs(wx) - gamma, 0) * np.sign(wx)
    return wp


#
def prox_L2(wx, gamma):
    wp = wx / (1 + gamma)
    return wp


# %%
def opL_1D(x, opt):
    le = len(x)
    xt = np.zeros(x.shape)

    if opt['filter'] == 'gradient':
        if opt['computation'] == 'fourier':
            h = np.array([1 / 2, -1 / 2])
            H = np.fft.fft(h, le)
            xt = np.real(np.fft.ifft(np.fft.fft(x) * H))
        elif opt['computation'] == 'direct':
            # working 1
            xt = np.append((x[1:] - x[:-1]) / 2, 0)
            # working 2
            # xt[1:] = (x[1:] - x[:-1]) / 2
            # xt[0] = -np.sum(xt[1:])

    elif opt['filter'] == 'laplacian':
        if opt['computation'] == 'fourier':
            h = np.array([1 / 4, -1 / 2, 1 / 4])
            H = np.fft.fft(h, le)
            xt = np.real(np.fft.ifft(np.fft.fft(x) * H))
            print(xt.shape)
        elif opt['computation'] == 'direct':
            xt[1:-1] = x[2:] / 4 - x[1:-1] / 2 + x[:-2] / 4

    # elif opt['filter'] == 'Mgradient':
    #     if opt['computation'] == 'fourier':
    #         h = np.array([1/2, 1/2, -1/2, -1/2])/2
    #         H = np.fft.fft(h, le)
    #         xt = np.real(np.fft.ifft(np.fft.fft(x) * H))
    #     elif opt['computation'] == 'direct':
    #         # working 1
    #         xt = np.append((x[1:] - x[:-1]) / 2, 0)
    #         # working 2
    #         # xt[1:] = (x[1:] - x[:-1]) / 2
    #         # xt[0] = -np.sum(xt[1:])

    return xt


#
def opLadj_1D(y, opt):
    le = len(y)
    x = np.zeros(y.shape)

    if opt['filter'] == 'gradient':
        if opt['computation'] == 'fourier':
            h = np.array([1 / 2, -1 / 2])
            H = np.fft.fft(h, le)
            x = np.real(np.fft.ifft(np.fft.fft(y) * np.conj(H)))
        elif opt['computation'] == 'direct':
            # working 1
            # x = -np.append(np.append(y[0]/2, (y[1:-1] - y[:-2])/ 2), -y[-2]/2)
            x = -np.append(0, (y[1:] - y[:-1]) / 2)
            # working 2
            # x[0:-1] = - (y[1:] - y[:-1]) / 2
            # x[-1] = -np.sum(x[0:-1])

    elif opt['filter'] == 'laplacian':
        if opt['computation'] == 'fourier':
            h = np.array([1 / 4, -1 / 2, 1 / 4])
            H = np.fft.fft(h, le)
            x = np.real(np.fft.ifft(np.fft.fft(y) * np.conj(H)))
        elif opt['computation'] == 'direct':
            x[1:-1] = (y[2:] / 4 - y[1:-1] / 2 + y[:-2] / 4)

    # elif opt['filter'] == 'Mgradient':
    #     if opt['computation'] == 'fourier':
    #         h = np.array([1/2, 1/2, -1/2, -1/2])/2
    #         H = np.fft.fft(h, le)
    #         x = np.real(np.fft.ifft(np.fft.fft(y) * np.conj(H)))
    #     elif opt['computation'] == 'direct':
    #         # working 1
    #         # x = -np.append(np.append(y[0]/2, (y[1:-1] - y[:-2])/ 2), -y[-2]/2)
    #         x = -np.append(0, (y[1:] - y[:-1]) / 2)
    #         # working 2
    #         # x[0:-1] = - (y[1:] - y[:-1]) / 2
    #         # x[-1] = -np.sum(x[0:-1])

    return x


# %%
def PD_ChambollePock(data, param, op, prox, objective, epsilon=1e-10):
    # Fixing Proximal Parameters
    # epsilon = 1e-10
    gamma = 0.99
    tau = gamma / param['normL']
    sig = gamma / param['normL']

    if tau * sig * param['normL'] ** 2 > 1:
        print('ERROR')

    theta = 1

    # Initializing variables
    x = np.zeros(data.shape)
    y = op['direct'](x)
    x0 = x
    bx = x

    # Criterion of convergence
    crit = np.zeros((param['iter'],))
    crit[0] = 0
    delta_crit = 1
    # print(crit.shape)
    # Algorithm
    for i in range(param['iter']):

        # Update of primal variable
        tmp = y + sig * op['direct'](bx)
        y = tmp - sig * prox['regularization'](tmp / sig, param['lambda'] / sig)
        # print(i, np.max(np.abs(y)))
        # Update of dual variable
        x = prox['fidelity'](x0 - tau * op['adjoint'](y), data, tau)

        # Update of the descent steps
        if param['mu'] >= 1:
            theta = (1 + 2 * param['mu'] * tau) ** (-1 / 2)
            tau = theta * tau
            sig = sig / theta

        # Update dual auxiliary variable
        bx = x + theta * (x - x0)
        x0 = x
        crit[i] = objective['fidelity'](x, data) + objective['regularization'](op['direct'](x), param['lambda'])
        if i > 1:
            delta_crit = np.abs(crit[i] - crit[i - 1]) / crit[i]
            # print(i,crit[i - 1],crit[i])
        # if delta_crit < epsilon:
        #    break
    # print(i, delta_crit,crit[i] )
    return x, crit

