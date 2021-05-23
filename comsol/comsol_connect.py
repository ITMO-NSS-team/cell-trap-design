# # -*- coding: utf-8 -*-
# """
# Created on Wed Feb  3 12:49:07 2021

import os

# @author: user
# """
import mph

from polygen import poly_add, poly_draw, random_poly

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

client = mph.Client(cores=1)

N_Vert = 5
N_poly = 3
box1 = [-150, -165, -25, 150];

poly_box=[]

for _ in range(N_poly):
    poly_box.append(random_poly(N_Vert,box1))

model = client.load('ML_add_curl_curv_May21_out.mph')


model=poly_add(model,poly_box)


model.build()

model.mesh()

model.solve()


poly_draw(model)
















