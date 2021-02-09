# # -*- coding: utf-8 -*-
# """
# Created on Wed Feb  3 12:49:07 2021
import gc
import os
from typing import Tuple
from uuid import uuid4

import numpy as np
import pickledb

from comsol.polygen import poly_draw
from core.structure.structure import Structure

# @author: user
# """

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import matplotlib.pyplot as plt
from core.utils import project_root
from core.utils import GlobalEnv

global_env = GlobalEnv


def poly_add(model, polygons):
    for n, poly in enumerate(polygons):
        try:
            model.java.component('comp1').geom('geom1').create('pol' + str(n + 1), 'Polygon')
        except Exception:
            pass
        model.java.component('comp1').geom('geom1').feature('pol' + str(n + 1)).set('x', poly[0])
        model.java.component('comp1').geom('geom1').feature('pol' + str(n + 1)).set('y', poly[1])
    return model


def execute(structure: Structure, with_vizualization=True) -> Tuple[float, str]:
    gc.collect()
    client = GlobalEnv.comsol_client
    target, idx = _load_fitness(structure)
    if target is None or GlobalEnv.full_save_load:
        model, idx = _load_simulation_result(structure)
        if model is None:
            poly_box = []

            for i, pol in enumerate(structure.polygons):
                poly_repr = []
                poly_repr.append(' '.join([str(pt.x) for pt in pol.points]))
                poly_repr.append(' '.join([str(pt.y) for pt in pol.points]))
                poly_box.append(poly_repr)

            model = client.load(f'{project_root()}/comsol/Comsol2pics_add_curl_curv.mph')

            try:
                model = poly_add(model, poly_box)

                model.build()
                model.mesh()
                model.solve()
            except Exception as ex:
                print(ex)
                client.clear()
                return 0.0

            idx = _save_simulation_result(structure, model)

        try:
            outs = [model.evaluate('vlct_1'),
                    model.evaluate('vlct_2'),
                    model.evaluate('vlct_3'),
                    model.evaluate('vlct_4'),
                    model.evaluate('vlct_5'),
                    model.evaluate('vlct_side'),
                    model.evaluate('vlct_main')]
        except Exception as ex:
            print(ex)
            client.clear()
            return 0.0

        u = model.evaluate('spf.U')
        curl = model.evaluate('curl')
        curv = model.evaluate('curv') / 10 ** 7

        fast_u_tresh = 0
        fast_u = np.mean(u[u > 0]) + (np.max(u) - np.mean(u[u > 0])) * fast_u_tresh
        width_ratio = len(u[u > fast_u]) / len(u[u > 0])

        outs = [float(_) for _ in outs]

        target = float(sum(outs[0:5])) / float(sum(outs[5:7]))
        if (curl > 30000) or ((width_ratio < 0.25) or (width_ratio > 0.34)):
            target = 0

        if with_vizualization and target > 0:
            x = model.evaluate('x')
            y = model.evaluate('y')
            u = model.evaluate('spf.U')
            lbl = f'{round(target, 4)}, \n {[round(_, 4) for _ in outs]}, \n ' \
                  f'{round(float(curl))}, {round(curv, 4)}, {round(width_ratio, 4)}'
            # plt.title(lbl)
            # plt.scatter(x, y, c=u, cmap=plt.cm.coolwarm)

            poly_draw(model)

            # vmin=0, vmax=0.003)
            # plt.colorbar()
            # plt.show()
            plt.savefig(f'./tmp/{target}.png')
            plt.clf()

        client.clear()

        _save_fitness(structure, target)
        if target > 0:
            print(round(target, 4), [round(_, 4) for _ in outs], round(float(curl)), \
                  round(curv, 4), round(width_ratio, 4))
    else:
        print(f'Cached: {target}')

    return target, idx


def _save_simulation_result(configuration, model):
    if not os.path.exists('./models'):
        os.mkdir('./models')
    model_uid = str(uuid4())
    model.save(f'./models/{model_uid}.mph')
    db = pickledb.load('comsol_db.saved', False)
    db.set(str(configuration), model_uid)
    db.dump()
    return model_uid


def _save_fitness(configuration, fitness):
    db = pickledb.load('fitness_db.saved', False)
    db.set(str(configuration), str(fitness))
    db.dump()


def _load_simulation_result(configuration):
    db = pickledb.load('comsol_db.saved', False)

    model_uid = db.get(str(configuration))

    if model_uid is False:
        return None, None

    model = GlobalEnv.comsol_client.load(f'./models/{model_uid}.mph')

    return model, model_uid


def _load_fitness(configuration):
    db = pickledb.load('fitness_db.saved', False)

    db_models = pickledb.load('comsol_db.saved', False)

    model_uid = db_models.get(str(configuration))

    fitness = db.get(str(configuration))

    if fitness is False:
        return None, None

    return float(fitness), model_uid


if False:
    from core.optimisation.operators import get_random_structure
    from core.structure.domain import Domain
    from core.utils import GlobalEnv

    domain = Domain(min_x=-140, max_x=-45, min_y=-165, max_y=50)
    GlobalEnv.domain = domain

    test_structure = get_random_structure(3, 3)
    print(test_structure)
    target = execute(test_structure)
    print(target)
