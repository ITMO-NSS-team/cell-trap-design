# # -*- coding: utf-8 -*-
# """
# Created on Wed Feb  3 12:49:07 2021

# @author: user
# """
import mph
from polygen import random_poly
from polygen import poly_add
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import jpype 

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

client = mph.Client(cores=1)

N_Vert=5
N_poly=5
box1 = [ -140, -165, -45, 50];

poly_box=[]

for _ in range(N_poly):
    poly_box.append(random_poly(N_Vert,box1))

    
model = client.load('Comsol2pics.mph')

model=poly_add(model,poly_box)

model.build()


model.mesh()


model.solve()

x=model.evaluate('x')
y=model.evaluate('y')
U=model.evaluate('spf.U')

target=model.evaluate('vlct_main')

print(target)

plt.scatter(x,y,U)

# mph.client.shutdown()


