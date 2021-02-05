# # -*- coding: utf-8 -*-
# """
# Created on Wed Feb  3 12:49:07 2021
import os
from uuid import uuid4

import numpy as np
import pickledb

# from comsol.polygen import poly_add
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


def execute(structure: Structure, with_vizualization=True) -> float:
    model = _load_simulation_result(structure)
    if model is None:
        client = GlobalEnv.comsol_client

        poly_box = []

        for i, pol in enumerate(structure.polygons):
            poly_repr = []
            # for j, pt in enumerate(pol.points):
            poly_repr.append(' '.join([str(pt.x) for pt in pol.points]))
            poly_repr.append(' '.join([str(pt.y) for pt in pol.points]))
            poly_box.append(poly_repr)

        model = client.load(f'{project_root()}/comsol/Comsol2pics_add_curl_curv.mph')

        model = poly_add(model, poly_box)

        model.build()
        model.mesh()
        model.solve()

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
        return 0.0

    u = model.evaluate('spf.U')
    curl = model.evaluate('curl')
    curv = model.evaluate('curv') / 10 ** 7

    fast_u_tresh = 0
    fast_u = np.mean(u[u > 0]) + (np.max(u) - np.mean(u[u > 0])) * fast_u_tresh
    width_ratio = len(u[u > fast_u]) / len(u[u > 0])

    outs = [float(_) for _ in outs]

    _save_simulation_result(structure, model)

    target = float(sum(outs[0:5])) / float(sum(outs[5:7]))
    if (curl > 30000) or ((width_ratio < 0.25) or (width_ratio > 0.34)):
        target = 0

    if with_vizualization:
        x = model.evaluate('x')
        y = model.evaluate('y')
        u = model.evaluate('spf.U')
        plt.title(round(target, 6))
        plt.scatter(x, y, c=u, cmap=plt.cm.coolwarm)
        # vmin=0, vmax=0.003)
        # plt.colorbar()
        # plt.show()
        plt.savefig(f'./tmp/{target}.png')
        plt.clf()

    print(target, [round(_, 5) for _ in outs], curl, curv, width_ratio)

    return target


def _save_simulation_result(configuration, model):
    if not os.path.exists('./models'):
        os.mkdir('./models')
    model_uid = str(uuid4())
    model.save(f'./models/{model_uid}.mph')
    db = pickledb.load('comsol_db.saved', False)
    db.set(str(configuration), model_uid)
    db.dump()


def _load_simulation_result(configuration):
    db = pickledb.load('comsol_db.saved', False)

    model_uid = db.get(str(configuration))

    if model_uid is False:
        return None

    model = GlobalEnv.comsol_client.load(f'./models/{model_uid}.mph')

    return model


def _load_simulation_result_reference_by_id(self, id):
    db = pickledb.load(self.model_results_file_name, False)
    for key in db.db:
        if db.db[key] == id:
            return key
    return None


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
