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


for _ in range(100):
    N_Vert=5
    N_poly=3
    box1 = [ -150, -165, -25, 150];
    
    poly_box=[]
    
    for _ in range(N_poly):
        poly_box.append(random_poly(N_Vert,box1))
    
        
    model = client.load('Comsol2pics_add_curl_curv.mph')
    
    model=poly_add(model,poly_box)
    
    try:
        model.build()
    except Exception:
        continue
    
    try:
        model.mesh()
    except Exception:
        continue
    
    
    
    try:
        model.solve()
    except Exception:
        continue
    
    x=model.evaluate('x')
    y=model.evaluate('y')
    U=model.evaluate('spf.U')
    
    fast_U_tresh=0
    
    fast_U=np.mean(U[U>0])+(np.max(U)-np.mean(U[U>0]))*fast_U_tresh
    
    width_ratio=len(U[U>fast_U])/len(U[U>0])
    
    target=(model.evaluate('vlct_1')+model.evaluate('vlct_2')+model.evaluate('vlct_3')+model.evaluate('vlct_4')+model.evaluate('vlct_5'))/(model.evaluate('vlct_main')+model.evaluate('vlct_side'))
    
    curv=model.evaluate('curv')/10**7
    
    curl=model.evaluate('curl')
    
    if ((curl>30000) or ((width_ratio<0.25) or (width_ratio>0.34))):
        continue
    
    print(f'target={target:2f} curv={curv:2f} curl={curl:2f} width_ratio={width_ratio:2f}')
    
    plt.figure()
    plt.scatter(x,y,c=U,cmap=plt.cm.coolwarm)
    plt.title(f'target={target:2f} curv={curv:2f} curl={curl:2f} width_ratio={width_ratio:2f}')


