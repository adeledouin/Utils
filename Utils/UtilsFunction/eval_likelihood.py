# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 16:50:55 2021

@author: Victor Levy dit Vehel, victor.levy.vehel [at] gmail [dot] com
"""

import numpy as np
import matplotlib.pyplot as plt
from math import erf
from scipy.optimize import curve_fit



def eval_network_likelihood(evt, network, im_g):
    source_likelihood = {} ; ll = []
    trashed_sensor = []
    for point in range(network.n_contact):
        print(point)
        try:
            shifts = network.reverse_propagation_shifts(point)
          #  shifts = np.reshape(np.array(shifts), (3,2)).mean(1)
          #  evt_n = np.reshape(np.array(evt), (3,2)).mean(1)
            ti = (np.array(evt) - np.array(shifts))

            tin = (np.array(evt) - np.array(shifts) - np.mean(evt) + np.mean(shifts))**2
            tin = np.delete(tin, tin.argmax())
            #tin = np.delete(tin, tin.argmax())

            trashed = []
            for i in []:
                tim = np.abs(ti - ti.mean())
                trashed += [tim.argmax()]
                ti = np.delete(ti, tim.argmax())
            trashed_sensor += [trashed]

            likelihood = (np.std(ti))
            #likelihood = np.mean(tin)
            x_source, y_source = network.x_c[point], network.y_c[point]
            source_likelihood[point] = [likelihood, x_source, y_source]
            ll+=[likelihood]
        except:
            source_likelihood[point] = [-1, network.x_c[point], network.y_c[point]]

    return source_likelihood, min(ll), max(ll), trashed_sensor

def eval_network_likelihood_smart(evt, d_evt, network, eps, weightmode = 'invR', agglomode='prod', exclude=[]):
    ttime = network.reverse_propagation_smart()
    #calc dtp_pred
    dt_meas = evt[:,None] - evt[None, :]
    sigma_meas = (d_evt[:,None]**2 + d_evt[None, :]**2)**.5
    filt_mat = (1 - np.tri(len(evt))).astype('bool')
    probas = np.zeros(network.n_contact)
    for pt in range(network.n_contact):
        #calc dt_meas
        dt_pred = ttime[:,pt][:,None] - ttime[:,pt][None, :]
        #calc sigma
        sigma_pred = 0.1*(ttime[:,pt][:,None]**2 + ttime[:,pt][None, :]**2)**.5
        sigma_mat = (sigma_pred**2 + sigma_meas**2)**.5
        E_mat = dt_meas - dt_pred

        for excluded in exclude:
            sigma_mat[:, excluded] = np.inf
            sigma_mat[excluded, :] = np.inf

        E = E_mat[filt_mat]
        S = sigma_mat[filt_mat]

        probas[pt] = prob_agglo(eps, E, S, weightmode, agglomode)
        m = np.nanmin(probas)
        probas[probas==1] = m
        probas[np.isnan(probas)] = m
    return probas


def eval_network_likelihood_indep(evt, d_evt, network, eps,
    weightmode = 'invR', agglomode='prod', exclude=[],
    sensors1 = [0,1,2], sensors2 = [3,4,5]):
    ttime = network.reverse_propagation_smart()
    #calc dtp_pred

    dt_meas = evt[sensors1] - evt[sensors2]
    sigma_meas = (d_evt[sensors1]**2 + d_evt[sensors2]**2)**.5

    probas = np.zeros(network.n_contact)
    for pt in range(network.n_contact):
        #calc dt_meas
        dt_pred = ttime[sensors1,pt] - ttime[sensors2, pt]
        #calc sigma
        sigma_pred = 0.1*(ttime[sensors1,pt]**2 + ttime[sensors2, pt]**2)**.5
        S = (sigma_pred**2 + sigma_meas**2)**.5
        E = dt_meas - dt_pred

        S = np.delete(S, exclude)
        E = np.delete(E, exclude)

        probas[pt] = prob_agglo(eps, E, S, weightmode, agglomode)
        m = np.nanmin(probas)
        #probas[probas==1] = m
        probas[np.isnan(probas)] = m
    return probas


def eval_network_likelihood_cont(evt, d_evt, network, eps, weightmode = 'invR', agglomode='prod', exclude=[]):

    #calc dtp_pred
    dt_meas = evt[[0, 1, 2]] - evt[[3, 4, 5]]
    sigma_meas = (d_evt[[0, 1, 2]]**2 + d_evt[[3, 4, 5]]**2)**.5

    xs = network.x_c[network.sensor_id]
    ys = network.y_c[network.sensor_id]

    x = network.x_c
    y = network.y_c

    D1 = (x-xs[0])**2 + (y-ys[0])**2
    D4 = (x-xs[3])**2 + (y-ys[3])**2
    D14 = D1**.5 - D4**.5
    D2 = (x-xs[1])**2 + (y-ys[1])**2
    D5 = (x-xs[4])**2 + (y-ys[4])**2
    D25 = D2**.5 - D5**.5
    D3 = (x-xs[2])**2 + (y-ys[2])**2
    D6 = (x-xs[5])**2 + (y-ys[5])**2
    D36 = D3**.5 - D6**.5


    probas = np.zeros(network.n_contact)
    for pt in range(network.n_contact):
        #calc dt_meas
        dt_pred =np.array([D14[pt], D25[pt], D36[pt]])/838.7249*2500000
        #calc sigma
        sigma_pred = 0#.1*(ttime[[0, 1, 2],pt]**2 + ttime[[3, 4, 5], pt]**2)**.5
        S = (sigma_pred**2 + sigma_meas**2)**.5
        E = dt_meas - dt_pred

        S = np.delete(S, exclude)
        E = np.delete(E, exclude)

        probas[pt] = prob_agglo(eps, E, S, weightmode, agglomode)
        m = np.nanmin(probas)
        #probas[probas==1] = m
        probas[np.isnan(probas)] = m
    return probas


def prob_agglo(eps, E, S, weightmode, agglomode):
    if agglomode=='prod':
        W = weights(S, weightmode)
        P = np.prod([ prob(eps, e, s)**w for e, s, w in zip(E, S, W) ])

    if agglomode=='prod_exp':
        W = weights(S, weightmode)
        P = np.prod([ prob(s, e, s)**w for e, s, w in zip(E, S, W) ])

    if agglomode=='max':

        P = np.nanmax([ prob(eps, e, s) for e, s in zip(E, S) ])
    if agglomode=='sum':
        W = weights(S, weightmode)
        P = np.sum([ prob(eps, e, s)*w for e, s, w in zip(E, S, W) ])

    if P==1:
        print(E)
        print(S)
        print(W)
    return P

def prob(eps, mu, sigma):
    """ return P(|x|<eps) for N(mu, sigma)"""
    return 0.5*(erf((eps - mu)/(sigma*2**.5)) - erf((-eps - mu)/(sigma*2**.5)))

def weights(S, weightmode):
    """ """
    if weightmode=='const':
        return S*0+1
    elif weightmode == 'inv':
        return 1/S
    elif weightmode == 'inv2':
        return 1/S**2
    elif weightmode == 'invR':
        return 1/S**.5

def plot_pred_smart(P, network, image, ratio):
    """ """
    X = network.x_c/ratio
    Y = network.y_c/ratio
    plt.scatter(Y, X, c=np.log(P), marker='o', cmap='flag')
    m=np.argmax(P)
    plt.plot(Y[m], X[m], marker='*', color='yellow', markersize='20')
    plt.imshow(image)


def plot_predictions(source_likelihood, max_likelihood, min_likelihood, network, im_g):
    """ plot the prediction results """
    fig, ax = plt.subplots()
    ax.imshow(im_g)

    ratio = network.ratio
    for x, y, r in zip(network.x_g, network.y_g, network.r_g):#zip(C*ratio, R*ratio):
        ax.add_artist(plt.Circle((y/ratio, x/ratio), r, fill=False, color = 'k'))

    X, Y, Z = [], [], []
    for k, v in zip(source_likelihood.keys(), source_likelihood.values()):
        col = (v[0] - min_likelihood)/(max_likelihood - min_likelihood)
        X += [v[2]] ; Y += [v[1]] ; Z += [col]
    X = np.array(X) ; Y = np.array(Y) ; Z = np.array(Z)

    ax.scatter(X/ratio, Y/ratio, c=Z, marker='o', cmap = 'gist_stern') #'gist_stern_r')
    #x0, y0, dx0, dy0 = find_best_source(X, Y, Z)
    #err = (dx0**2 + dy0**2)**0.5

    #ax.add_artist(plt.Circle((x0/ratio, y0/ratio), 3*err/ratio, fill=1, alpha= 0.25, color = 'yellow'))
    #ax.add_artist(plt.Circle((x0/ratio, y0/ratio), 2*err/ratio, fill=1, alpha= 0.25, color = 'red'))
    #ax.add_artist(plt.Circle((x0/ratio, y0/ratio), err/ratio, fill=1, alpha= 0.5, color = 'magenta'))
    #plt.plot(x0/ratio, y0/ratio, 'ko')
    plt.title(str(min_likelihood) +'_' + str(max_likelihood))
    plt.axis('equal')


def plot_paths(network, xs, ys, **kwargs):
    """ plot theoritical sound path """
    dist = ((network.x_c - xs)**2 + (network.y_c - ys)**2 ) **0.5
    source = dist.argmin()
    ratio = network.ratio
    plt.plot(xs, ys, 'ko')
    for sensor in network.sensor_id:
        path = network.find_path(source, sensor)
        line_x, line_y = [], []
        for point in path:
            line_x += [network.y_c[point]/ratio]
            line_y += [network.x_c[point]/ratio]
        line_x, line_y = np.array(line_x), np.array(line_y)
        dx, dy = np.random.randn(2)*0.001/ratio
        plt.plot(line_x, line_y, linewidth=4)



def find_best_source(X, Y, Z, min_dist = 0.04):
    """ Takes Z=f(X,Y) as input and perform a simple 2nd order polynomial fit
        to find the most likely center. Only takes X and Y data that are at most
        min_dist away from Z_max position. """

    # fonction de fit
    def poly(xy_mesh, xc, yc, x2, y2, x1y1):
        (x, y) = xy_mesh
        X2 = x2 * (x-xc)**2
        Y2 = y2 * (y-yc)**2
        XY = x1y1 * (x-xc)*(y-yc)
        OFF = np.ones_like(x)
        return X2 + Y2 + XY + OFF

    z_max = Z.max()
    where_max = (Z == z_max)
    Xm, Ym = X[where_max].mean(), Y[where_max].mean()

    d = ( (X - Xm)**2 + (Y - Ym)**2 ) ** 0.5
    f = d < min_dist
    s2 = - Z[f].min() / min_dist**2
    guess_vals = [Xm, Ym, s2, s2, 0]
    xy_mesh= (X[f], Y[f])
    data = Z[f]
    fit_params, cov_mat = curve_fit(poly, xy_mesh, data, p0=guess_vals)
    return fit_params[0], fit_params[1], cov_mat[0,0]**.5, cov_mat[1,1]**.5


def eval_source_likelihood(grain_signal):
    """
    likelihoods:
        dictionnaire. Clé == numéros des contacts
            valeurs = [probabilité, temps, x, y]
    """
#    sig = convolve(grain_signal, np.ones(tolerance, dtype=np.int8),'same')
#    ind = (sig>5).astype(np.int8)
#    if ind.max() !=0:
#        whr = np.diff(ind)==-1
#        likelihood, times = np.cumsum(ind)[:-1][whr][0], np.where(whr==True)[0]
#        return likelihood, times
#    else:
#        return 0,0
    ind = np.where(grain_signal==1)
    return np.var(ind)# ind[0][0] - ind[0][-1], np.mean(ind[0])
