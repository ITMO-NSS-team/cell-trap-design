# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:48:49 2021

@author: user
"""
import matplotlib.pyplot as plt
import numpy as np

from comsol.geometry import (bnds_up, bnds_down, rumb,
                             trap_1, trap_2, trap_3,
                             trap_4, trap_5)


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


def poly_add(model, polygons):
    for n, poly in enumerate(polygons):
        try:
            model.java.component('comp1').geom('geom1').create('pol' + str(n + 1), 'Polygon')
        except Exception:
            pass
        model.java.component('comp1').geom('geom1').feature('pol' + str(n + 1)).set('x', poly[0])
        model.java.component('comp1').geom('geom1').feature('pol' + str(n + 1)).set('y', poly[1])
    return model


def poly_sort(vertices):
    vertices = np.array(vertices)
    x_cent = np.mean(vertices[:, 0])
    y_cent = np.mean(vertices[:, 1])
    vertices[:, 0] = vertices[:, 0] - x_cent
    vertices[:, 1] = vertices[:, 1] - y_cent
    vertices_comp = vertices[:, 0] + 1j * vertices[:, 1]
    vertices = vertices[np.argsort(np.angle(vertices_comp))]
    vertices[:, 0] = vertices[:, 0] + x_cent
    vertices[:, 1] = vertices[:, 1] + y_cent
    return vertices


def poly_draw(model, sort=False):
    x_up, y_up = zip(*bnds_up)

    x_down, y_down = zip(*bnds_down)

    x_rumb, y_rumb = zip(*rumb)

    x_trap_1, y_trap_1 = zip(*trap_1)

    x_trap_2, y_trap_2 = zip(*trap_2)

    x_trap_3, y_trap_3 = zip(*trap_3)

    x_trap_4, y_trap_4 = zip(*trap_4)

    x_trap_5, y_trap_5 = zip(*trap_5)
    x = model.evaluate('x')
    y = model.evaluate('y')
    U = model.evaluate('spf.U')

    plt.figure()
    plt.scatter(x[U > 0], y[U > 0], c=U[U > 0], cmap=plt.cm.coolwarm)
    plt.plot(x_up, y_up, linewidth=6, c='black')
    plt.plot(x_down, y_down, linewidth=6, c='black')
    plt.plot(x_rumb, y_rumb, linewidth=6, c='black')
    plt.plot(x_trap_1, y_trap_1, linewidth=6, c='black')
    plt.plot(x_trap_2, y_trap_2, linewidth=6, c='black')
    plt.plot(x_trap_3, y_trap_3, linewidth=6, c='black')
    plt.plot(x_trap_4, y_trap_4, linewidth=6, c='black')
    plt.plot(x_trap_5, y_trap_5, linewidth=6, c='black')

    i = 1
    while True:
        try:
            xpoly_str = str(model.java.component('comp1').geom('geom1').feature('pol' + str(i)).getString('x'))
        except Exception:
            break

        xpoly = np.array(xpoly_str.split(), dtype=np.float)
        ypoly_str = str(model.java.component('comp1').geom('geom1').feature('pol' + str(i)).getString('y'))
        ypoly = np.array(ypoly_str.split(), dtype=np.float)

        vertices = np.transpose(np.vstack((xpoly, ypoly)))

        if sort:
            vertices = poly_sort(np.transpose(np.vstack((xpoly, ypoly))))

        vertices = np.vstack((vertices, vertices[0]))

        xpoly, ypoly = zip(*vertices)

        plt.plot(xpoly, ypoly, linewidth=6, c='magenta')
        i += 1

    fast_U_tresh = 0

    fast_U = np.mean(U[U > 0]) + (np.max(U) - np.mean(U[U > 0])) * fast_U_tresh

    width_ratio = len(U[U > fast_U]) / len(U[U > 0])

    target = (model.evaluate('vlct_1') + model.evaluate('vlct_2') + model.evaluate('vlct_3') + model.evaluate(
        'vlct_4') + model.evaluate('vlct_5')) / (model.evaluate('vlct_main') + model.evaluate('vlct_side'))

    curv = model.evaluate('curv') / 10 ** 7

    curl = model.evaluate('curl')

    plt.title(f'target={target:2f} curv={curv:2f} curl={curl:2f} width_ratio={width_ratio:2f}')
