# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:48:49 2021

@author: user
"""
import numpy as np


def random_poly(N_vert, box):
    x1 = box[0]
    y1 = box[1]
    x2 = box[2]
    y2 = box[3]
    xnum = np.random.uniform(low=x1, high=x2, size=N_vert)
    ynum = np.random.uniform(low=y1, high=y2, size=N_vert)
    xstr = str(xnum[0])
    ystr = str(ynum[0])
    for i in range(1, N_vert):
        xstr += (' ' + str(xnum[i]))
        ystr += (' ' + str(ynum[i]))
    return [xstr, ystr]
