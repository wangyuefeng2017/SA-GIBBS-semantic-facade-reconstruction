# -*- coding: utf-8 -*-
"""
Created on Sun May  3 19:15:10 2020

@author: wyf-laptop
"""
import numpy as np
import first0
import random
import os
def ransac(data,maxD,time):
    iteration=0
    face=[]
    
    while iteration<=time:
        p1,p2,p3=random.sample(range(0,len(data)),3) # randomly choosing 3 points
        x1,y1,z1=data[p1][0:3]
        x2,y2,z2=data[p2][0:3]
        x3,y3,z3=data[p3][0:3]
        if (x2-x1)*(y3-y2) != (y2-y1)*(x3-x2): # judge whether the three points are in one line or not.
            face_new=[]
            A_t = (y2 - y1)*(z3 - z1) - (z2 - z1)*(y3 - y1)
            B_t = (x3 - x1)*(z2 - z1) - (x2 - x1)*(z3 - z1)
            C_t = 0#(x2 - x1)*(y3 - y1) - (x3 - x1)*(y2 - y1) 
            # considering that facade is perpendicular to ground, so the parameter of Z-axis can be set to 0.
            D_t = -(A_t * x1 + B_t * y1 + C_t * z1)
            temp = np.sqrt(A_t*A_t + B_t*B_t + C_t*C_t)
            
            for i in range(len(data)):
                temp_D = abs(A_t*data[i][0] + B_t*data[i][1] + C_t*data[i][2] + D_t)/temp
                if temp_D<maxD: # count the points in proposial plane, if current plane have more points than previoud one, then replace it.
                    face_new.append(data[i])
            if len(face_new)>len(face):
                face=face_new
        iteration+=1
        print ('size of face:  ', len(face_new),len(face))
    return A_t, B_t, C_t, D_t,face


ii=1
filename=r"../example/original_facade_02.txt"
savepath=r'../example/ransacframe/'
# filename=r"D:\PCL_DATA\example\sph\\window_face_reflect_5.txt"
if not os.path.exists(savepath):
        os.makedirs(savepath)
        
data0=first0.get_data(filename)

A_t, B_t, C_t, D_t, face0 = ransac(data0,1,10)

temp = np.sqrt(A_t*A_t + B_t*B_t + C_t*C_t)
face=data0
face_new=[]
face2=[]
face3=[]
face4=[]
face5=[]
for i in range(len(face)):
    temp_D = abs(A_t*face[i][0] + B_t*face[i][1] + C_t*face[i][2] + D_t)/temp  # set a distance between points to optimal plane
    if 0.6>temp_D>0.2 and A_t*face[i][0] + B_t*face[i][1] + C_t*face[i][2] + D_t>0: # the points beyond the palne.
        face2.append(face[i])
    elif  0.6>temp_D>=0.2 and A_t*face[i][0] + B_t*face[i][1] + C_t*face[i][2] + D_t<=0: # the points belongs to windows
        face3.append(face[i])
    elif temp_D<0.2 and A_t*face[i][0] + B_t*face[i][1] + C_t*face[i][2] + D_t>0: 
        face4.append(face[i])
    elif temp_D<=0.2 and A_t*face[i][0] + B_t*face[i][1] + C_t*face[i][2] + D_t<=0:
        face5.append(face[i])


first0.write_data(face2,savepath+'window'+'_'+str(ii)+'_1.txt')
first0.write_data(face3,savepath+'window'+'_'+str(ii)+'_2.txt')
first0.write_data(face4,savepath+'window'+'_'+str(ii)+'_3.txt')
first0.write_data(face5,savepath+'window'+'_'+str(ii)+'_4.txt')
first0.write_data(face0,savepath+'window_face'+'_'+str(ii)+'.txt')
