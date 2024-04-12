#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 13:37:18 2021

@author: bastienvoirin
"""
import numpy as np
from matplotlib import pyplot as plt

def filter_particles(corners, C, R):
    """
    left_bottom, left_top, top_left, top_right, right_top, right_bottom, bottom_left, bottom_right = corners
    """
    #C[:,0],C[:,1]=C[:,1],C[:,0]
    
    C = np.roll(C, axis=1, shift=1)
    
    
    lb, lt, tl, tr, rt, rb, bl, br = corners
    
    l = lt - lb
    t = tr - tl
    r = rb - rt
    b = bl - br
    
    normal_l = np.array([-l[1], l[0]]) # vecteur perpendiculaire au segment de gauche
    normal_t = np.array([-t[1], t[0]]) # vecteur perpendiculaire au segment du haut
    normal_r = np.array([-r[1], r[0]]) # vecteur perpendiculaire au segment de droite
    normal_b = np.array([-b[1], b[0]]) # vecteur perpendiculaire au segment du bas
    
    cl = (lt+lb)/2
    ct = (tl+tr)/2
    cr = (rt+rb)/2
    cb = (bl+br)/2
    
    # Pour chaque centre C détecté, on calcule le produit scalaire de :
    # 1) C-lb avec normal_l : si c'est positif le centre est plus à gauche que le bord gauche
    # 2) C-tl avec normal_t : si c'est positif le centre est plus haut que le bord du haut
    # 3) C-rt avec normal_r : si c'est positif le centre est plus à droite que le bord droit
    # 4) C-br avec normal_t : si c'est positif le centre est plus bas que le bord du bas
    
    zeros = np.zeros(C.shape[0])
    prod_l = np.maximum(zeros, np.dot(C-lb, normal_l)) # ReLU
    prod_t = np.maximum(zeros, np.dot(C-tl, normal_t)) # ReLU
    prod_r = np.maximum(zeros, np.dot(C-rt, normal_r)) # ReLU
    prod_b = np.maximum(zeros, np.dot(C-br, normal_b)) # ReLU
    
    mask = (prod_l + prod_t + prod_r + prod_b) <= 0 # vrais centres = centres[mask <= 0]
    return C[mask,:], R[mask], mask