#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 17:17:02 2023

@author: sroux
"""

# import libraries
from Utils.Module.TraitementSignal.FiltrageNonLineaire import *
# from pypher.pypher import psf2otf


# %% ------------------ 1- Synthetic denoising

# %% ------- 1.1. Generate data
# Generate data
N = 2 ** 10  # 1000#2**15
SNR = 3
xmax = 1
xmin = 0
p = 0.012

s = (xmax - xmin) / (3 * SNR)
n = s * np.random.randn(N)
K = int(p * N)
t = np.random.rand(2 * K) * 2 / p
t = t
T = np.cumsum(t)
T = np.round(T[T <= 1.5 * N])
mu = (xmax - xmin) * np.random.rand(len(T)) + xmin
x = np.zeros(N)
for i in range(1, len(T)):
    x[T[i - 1].astype(int) + 1:T[i].astype(int)] = mu[i]
x = x.astype(float)
data = x + n

# plt.plot(data)
print(data.shape)

# %% ------- 1.2. Strong versus not strong convexity

# Strong versus not strong convexity
# Parameters
param = {
    'filter': 'gradient',
    'computation': 'fourier',
    'p': 1,
    'q': 1,
    'lambda': 10,
    'iter': 2000
}

# Algorithm
param['normL'] = 1
param['mu'] = 0
# Define operators and functions for optimization
# (You will need to implement the prox_L1, prox_L2, opL_1D, and opLadj_1D functions)
op = {
    'direct': lambda x: opL_1D(x, param),
    'adjoint': lambda x: opLadj_1D(x, param)
}

if param['p'] == 1:
    prox_fidelity = lambda y, data, tau: prox_L1(y - data, tau) + data
    objective_fidelity = lambda y, data: np.sum(np.abs(y - data))
elif param['p'] == 2:
    param['mu'] = 1
    prox_fidelity = lambda y, data, tau: prox_L2(y - data, tau) + data
    objective_fidelity = lambda y, data: 0.5 * np.sum(np.abs(y - data) ** 2)

if param['q'] == 1:
    prox_regularization = lambda y, tau: prox_L1(y, tau)
    objective_regularization = lambda y, tau: tau * np.sum(np.abs(y))
elif param['q'] == 2:
    prox_regularization = lambda y, tau: prox_L2(y, tau)
    objective_regularization = lambda y, tau: tau * np.sum(np.abs(y) ** 2)

prox = {
    'fidelity': prox_fidelity,
    'regularization': prox_regularization
}
objective = {
    'fidelity': objective_fidelity,
    'regularization': objective_regularization
}

# Perform optimization (You will need to implement PD_ChambollePock)
x1, crit1 = PD_ChambollePock(data, param, op, prox, objective, epsilon=1e-6)
param['mu'] = 1
x2, crit2 = PD_ChambollePock(data, param, op, prox, objective, epsilon=1e-6)

# Display results
plt.figure(1)
plt.clf()
plt.subplot(211)
plt.plot(data, color=[0.8, 0.8, 0.8])
plt.plot(x1, 'r')
plt.plot(x2, 'b')
plt.grid(True)
plt.title('Impact of strong convexity for piecewise constant estimation')

plt.subplot(212)
plt.semilogy(crit1, linewidth=2, color='r')
plt.gca().set_prop_cycle(None)  # Réinitialiser le cycle de couleur
plt.semilogy(crit2, linewidth=2, color='b')
plt.legend(['without strong convexity', 'with strong convexity'])
plt.grid(True)
plt.show()

# %% ------- 1.3. Impact of regularization parameter
# Impact of linear operator
# Parameters
param = {
    'filter': 'gradient',
    'computation': 'fourier',
    'p': 1,
    'q': 1,
    'lambda': 30,
    'iter': 2000
}

# Algorithm
param['normL'] = 1
param['mu'] = 1

# Perform optimization
x3, crit3 = PD_ChambollePock(data, param, op, prox, objective, epsilon=1e-6)

# Display results
plt.figure(2)
plt.subplot(211)
plt.plot(data, color=[0.8, 0.8, 0.8])
# plt.hold()
plt.plot(x2, 'r')
plt.plot(x3, 'b')
plt.grid()
plt.title('Impact of regularization parameter')

plt.subplot(212)
plt.semilogy(crit2, linewidth=2, color='r')
# plt.hold()
plt.semilogy(crit3, linewidth=2, color='b')
plt.legend(['Small lambda', 'Large lambda'])

plt.show()

# %% ------- 1.4. Impact of linear operator
# Impact of linear operator
# Parameters
param = {
    'filter': 'laplacian',
    'computation': 'fourier',
    'p': 1,
    'q': 1,
    'lambda': 100,
    'iter': 2000
}

# Algorithm
param['normL'] = 1
param['mu'] = 1

# Perform optimization
x4, crit4 = PD_ChambollePock(data, param, op, prox, objective, epsilon=1e-6)

# Display results
plt.figure(3)
plt.clf()
plt.subplot(211)
plt.plot(data, color=[0.8, 0.8, 0.8])
# plt.hold(True)
plt.plot(x2, 'r')
plt.plot(x4, 'b')
plt.grid(True)
plt.title('Impact of piecewise linear/constant estimation')

plt.subplot(212)
plt.semilogy(crit2, linewidth=2, color='r')
# plt.hold(True)
plt.semilogy(crit4, linewidth=2, color='b')
plt.legend(['D : finite difference', 'D laplacian'])

plt.show()

# %%
param = {
    'filter': 'laplacian',
    'computation': 'direct',
    'lambda': 100,
    'iter': 2000,
    'normL': 1,
    'mu': 1
}

# Perform optimization
x5, crit5 = PD_ChambollePock(data, param, op, prox, objective, epsilon=1e-6)
# Display results
plt.figure(4)
plt.clf()
plt.subplot(211)
plt.plot(data, color=[0.8, 0.8, 0.8])
# plt.hold(True)
plt.plot(x4, 'r')
plt.plot(x5, 'b')
plt.grid(True)
plt.title('Fourier/Direct')

plt.subplot(212)
plt.semilogy(crit5, linewidth=2, color='r')
# plt.hold(True)
plt.semilogy(crit4, linewidth=2, color='b')
plt.legend(['D : finite difference', 'D laplacian'])

plt.show()

# %% ------------------ 2- Real stick-slip data

# %% ------- 2.1. load the data
# Load data
kstiff = 168
vitesse = 42
dir = '/Users/sroux/latex/Cours/coursTS/M1/cours2023/FiltrageNonLineaire/stickslip-master/data_raw/'
tit = f'k{kstiff}Nm_v{vitesse}.mat'

fp = scipy.io.loadmat(dir + tit)
data_raw = scipy.io.loadmat(dir + tit)['Fnorm'].flatten()
data_raw = data_raw.astype(np.float64)
# Parameters
m = 30.7e-3
fa = 2e3
g = 9.81
th_noise = 40

# Display message
msg1 = 'EXAMPLE 1'
msg2 = 'nonlinear vs. linear denoising + t_start and t_stop detection'
msg3 = f'for a STICK-SLIP REGIME [k = {kstiff} N/m; V = {vitesse} microns/s].'

print('-------------------------------------------------------------------')
print(msg1)
print(msg2)
print(msg3)
print('-------------------------------------------------------------------')
print('Computing nonlinear & linear filtering...')

print(len(data_raw), np.mean(data_raw), data_raw.shape)

# %%  Algorithm L2L1: proposed method, non-linear filtering
param = {
    'filter': 'laplacian',
    'computation': 'direct',
    'lambda': 100,
    'iter': 20000,
    'normL': 1,
    'mu': 1
}

# Perform optimization
xl2l1, cc = PD_ChambollePock(data_raw[0:2 ** 16], param, op, prox, objective)

# xl2l1_data, cc = PD_ChambollePock(data, param, op, prox, objective)

# plt.plot(np.log(cc))
print('-- end ChambollePock')

# Extract tau_m and tau_s for L2L1
Fnorm = np.copy(xl2l1)
vp = -(fa * m * g * 1e6 / kstiff * (np.diff(Fnorm)) - vitesse)
t = np.linspace(0, len(Fnorm) - 1, len(Fnorm)) / fa
# start, stop, taus, taum = detect_tstartstop(Fnorm, g, vitesse, kstiff, m, fa, th_noise)
print('-- end extraction times')

#  Display figure
plt.figure(5)
plt.clf()
# ax1 = plt.subplot(121)
plt.plot(t, data_raw[0:2 ** 16], color=[0.0417, 0, 0], label='data')
plt.plot(t, Fnorm, color=[1, 0.45, 0], linewidth=1.5, label='optimal lambda')
# plt.plot(t[start], Fnorm[start], 'ok', markersize=7, markerfacecolor=[1, 1, 1], label='t_start')
# plt.plot(t[stop], Fnorm[stop], 'ok', markersize=7, markerfacecolor=[.7, .7, .7], label='t_stop')
plt.title('Nonlinear denoising: L2L1')
plt.xlabel('$t$ [s]', fontsize=16)
plt.ylabel('$F/mg$ [-]', fontsize=16)
plt.legend(loc='upper left')

# %%

