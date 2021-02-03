# # -*- coding: utf-8 -*-
# """
# Created on Wed Feb  3 12:49:07 2021
import os
from typing import List

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
    try:
        saved_result = _load_simulation_result(structure)
        if saved_result is not None:
            speeds = saved_result
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

            speeds = [model.evaluate('vlct_1'),
                      model.evaluate('vlct_2'),
                      model.evaluate('vlct_3'),
                      model.evaluate('vlct_4'),
                      model.evaluate('vlct_5'),
                      model.evaluate('vlct_side'),
                      model.evaluate('vlct_main')]

            speeds = [float(_) for _ in speeds]

            _save_simulation_result(structure, speeds)

            target = float(sum(speeds[0:5])) / float(sum(speeds[5:7]))

            if with_vizualization:
                x = model.evaluate('x')
                y = model.evaluate('y')
                U = model.evaluate('spf.U')
                plt.title(round(target, 6))
                plt.scatter(x, y, c=U, cmap=plt.cm.coolwarm,
                            vmin=0, vmax=0.003)
                # plt.colorbar()
                #plt.show()
                plt.savefig(f'./tmp/{target}.png')
                plt.clf()

        target = float(sum(speeds[0:5])) / float(sum(speeds[5:7]))
        print(target, [round(_, 5) for _ in speeds])
    except Exception as ex:
        print(ex)
        target = 0

    return target


def _save_simulation_result(configuration, target: List[float]):
    db = pickledb.load('comsol_db.saved', False)
    db.set(str(configuration), ' '.join([str(_) for _ in target]))
    db.dump()


def _load_simulation_result(configuration):
    db = pickledb.load('comsol_db.saved', False)

    target_str = db.get(str(configuration))

    if target_str is False:
        return None

    target = [float(_) for _ in target_str.split(' ')]

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
