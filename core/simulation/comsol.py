# # -*- coding: utf-8 -*-
# """
# Created on Wed Feb  3 12:49:07 2021
import os
from multiprocessing import Lock

import pickledb

# from comsol.polygen import poly_add
from core.structure.structure import Structure

# @author: user
# """

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import matplotlib.pyplot as plt
from core.utils import project_root


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
    saved_result = _load_simulation_result(structure)
    if saved_result is not None:
        target = saved_result
    else:
        client = GlobalEnv.comsol_client

        poly_box = []

        for i, pol in enumerate(structure.polygons):
            poly_repr = []
            # for j, pt in enumerate(pol.points):
            poly_repr.append(' '.join([str(pt.x) for pt in pol.points]))
            poly_repr.append(' '.join([str(pt.y) for pt in pol.points]))
            poly_box.append(poly_repr)

        model = client.load(f'{project_root()}/comsol/Comsol2pics.mph')

        model = poly_add(model, poly_box)

        model.build()
        model.mesh()
        model.solve()

        target = model.evaluate('vlct_main')
        _save_simulation_result(structure, float(target))

        if with_vizualization:
            x = model.evaluate('x')
            y = model.evaluate('y')
            U = model.evaluate('spf.U')

            plt.scatter(x, y, c=U, cmap=plt.cm.coolwarm)
            plt.show()

    return float(target)


def _save_simulation_result(configuration, target: float):
    lock = Lock()
    lock.acquire()

    db = pickledb.load('comsol_db.saved', False)
    db.set(str(configuration), target)
    db.dump()


def _load_simulation_result(configuration):
    db = pickledb.load('comsol_db.saved', False)

    target = db.get(str(configuration))

    if target is False:
        return None

    return target


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
