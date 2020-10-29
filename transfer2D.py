# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:06:45 2020

@author: wyf-laptop
"""

import first0
import numpy as np
# import filter_ransac1

def getplane_old(filename): # choose this function when the solpe of facade plane on o-xy is positive.
    data=first0.get_data(filename) #obtain 3D coordinates
    # A_t, B_t, C_t, D_t, face = filter_ransac1.ransac(data,0.5,10)
    data_xyz=[]
    for i in range(len(data)):
        data_xyz.append(data[i][0:3])
        
    data_xyz=[]
    xset=[]
    yset=[]
    zset=[]
    for i in range(len(data)):
        data_xyz.append(data[i][0:3])
        xset.append(data[i][0])
        yset.append(data[i][1])
        zset.append(data[i][2])
        
    xmax=max(xset)
    xmin=min(xset)
    ymax=max(yset)
    ymin=min(yset)

    x_new=[]
    y_new=[]
    for i in range(len(data_xyz)): #mapping a point into 2D plane, i.e. o-yz, and transfered it to new coordinates system.
        x_new.append(round(np.sqrt((data_xyz[i][0]-xmin)**2+(data_xyz[i][1]-ymin)**2),2))
        y_new.append(round(data_xyz[i][2],2))
    return x_new,y_new

def getplane_new(filename): # choose this function when the solpe of facade plane on o-xy is negative.
    data=first0.get_data(filename)
    # A_t, B_t, C_t, D_t, face = filter_ransac1.ransac(data,0.5,10)
    data_xyz=[]
    for i in range(len(data)): #obtain 3D coordinates
        data_xyz.append(data[i][0:3])
        
    data_xyz=[]
    xset=[]
    yset=[]
    zset=[]
    for i in range(len(data)):
        data_xyz.append(data[i][0:3])
        xset.append(data[i][0])
        yset.append(data[i][1])
        zset.append(data[i][2])
        
    xmax=max(xset)
    xmin=min(xset)
    ymax=max(yset)
    ymin=min(yset)

    x_new=[]
    y_new=[]
    for i in range(len(data_xyz)): #mapping a point into 2D plane, i.e. o-yz, and transfered it to new coordinates system.
        x_new.append(round(np.sqrt((data_xyz[i][0]-xmin)**2+(data_xyz[i][1]-ymax)**2),2))
        y_new.append(round(data_xyz[i][2],2))
        
    return x_new,y_new