# -*- coding: utf-8 -*-
"""
Created on Thu May 09 16:46:53 2019

@author: wpc
"""
import random
import numpy as np


def ransac(data,maxD,time):
    iteration=0
    face=[]
    
    while iteration<=time:
        p1,p2,p3=random.sample(range(0,len(data)),3)# randomly choosing 3 points
        x1,y1,z1=data[p1][0:3]
        x2,y2,z2=data[p2][0:3]
        x3,y3,z3=data[p3][0:3]
        if (x2-x1)*(y3-y2) != (y2-y1)*(x3-x2): # judge whether the three points are in one line or not.
            face_new=[]
            A_t = (y2 - y1)*(z3 - z1) - (z2 - z1)*(y3 - y1)
            B_t = (x3 - x1)*(z2 - z1) - (x2 - x1)*(z3 - z1)
            C_t = (x2 - x1)*(y3 - y1) - (x3 - x1)*(y2 - y1)
            D_t = -(A_t * x1 + B_t * y1 + C_t * z1)
        
            temp = np.sqrt(A_t*A_t + B_t*B_t + C_t*C_t)
            
            for i in range(len(data)):
                temp_D = abs(A_t*data[i][0] + B_t*data[i][1] + C_t*data[i][2] + D_t)/temp
                if temp_D<maxD:# count the points in proposial plane, if current plane have more points than previoud one, then replace it.
                    face_new.append(data[i])
            if len(face_new)>len(face):
                face=face_new
        iteration+=1
        print ('size of face:  ', len(face_new),len(face))
    return A_t, B_t, C_t, D_t,face


def point_face(point,face):
    A_t,B_t,C_t,D_t=face
    
    temp = np.sqrt(A_t*A_t + B_t*B_t + C_t*C_t)
    space = abs(A_t*point[0] + B_t*point[1] + C_t*point[2] + D_t)/temp
    
    return space

