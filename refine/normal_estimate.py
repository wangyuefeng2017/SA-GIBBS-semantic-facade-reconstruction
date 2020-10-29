# -*- coding: utf-8 -*-
"""
Created on Sun May  3 19:13:59 2020

@author: wyf-laptop
"""

import first0
import numpy as np
import filter_ransac1
import os

def getplane(filename):
    data=first0.get_data(filename) # obtain 3D coordinates
    A_t, B_t, C_t, D_t, face = filter_ransac1.ransac(data,0.5,10) # calculate optimal plane
    data_xyz=[]
    for i in range(len(face)):
        data_xyz.append(face[i][0:3])
    x_new=[]
    y_new=[]
    for i in range(len(data_xyz)): # transfer the 3D to 2D plane, where x- of 3D coordinate is set to 0.
        x_new.append(round(np.sqrt(data_xyz[i][0]**2+data_xyz[i][1]**2),2))
        y_new.append(round(data_xyz[i][2],2))
    return x_new,y_new,data_xyz

def direct(vector,mo,thr): # normal directions
    x,y,z= vector
    
    if mo>=thr: # according to the vector, noral direction can be determined
        if x>=0 and y>=0 and z>=0:
            d=8
        elif x>=0 and y<=0 and z>=0:
            d=1
        elif x<=0 and y>=0 and z>=0:
            d=2
        elif x<=0 and y<=0 and z>=0:
            d=3
        elif x>=0 and y>=0 and z<=0:
            d=4
        elif x>=0 and y<=0 and z<=0:
            d=5
        elif x<=0 and y>=0 and z<=0:
            d=6
        elif x<=0 and y<=0 and z<=0:
            d=7
    else:
        d=0
    
    return d
 
def spatial_sp(p1,p2,thr): # spatial spacing between two adjacent points
    
    
    x1,y1,z1=p1[0:3]
    x2,y2,z2=p2[0:3]
    distance=np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)
    
    vector=(x1-x2,y1-y2,z1-z2)
    direction=direct(vector,1/distance,thr)

    return direction
        
def temporl_sp(p1,p2,th2):
    t1=p1[7]
    t2=p2[7]
    
    if t1-t2<=th2:
        sp_t=0
    else:
        sp_t=1
    return sp_t

def unorder(filename): # produce the unorder point cloud
    data=first0.get_data(filename)
    data=sorted(data)
    init=0
    strip={}
    strip_data=[]
    for i in range(len(data)):
        if data[i][0]!=data[init][0]:
            strip[init]=strip_data
            init+=i-init
            if init>=len(data):
                break
            strip_data=[]
        else:
            strip_data.append(data[i])
    for k in strip.keys():
        subdata=strip[k]
        # print k
        direction_set=[]
        for i in range(1,len(subdata)-1):
            p1=subdata[i]
            p2=subdata[i-1]
            # p3=subdata[i+1]
            vector1=spatial_sp(p1,p2)
            mo=np.sqrt((vector1[0])**2+(vector1[1])**2+(vector1[2])**2)
            direction=direct(vector1,mo,0.4)
            direction_set.append(direction)
            

def create(filename,savepath): # save points according to normal directions
    x_new,y_new,data=getplane(filename)
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    direction_set=[]
    time_set=[]
    for i in range(1,len(data)):
        p1=data[i]
        p2=data[i-1]
        direction=spatial_sp(p1,p2,0.05)
        # sp_t=temporl_sp(p1,p2,0.001)
        direction_set.append(direction)
        # time_set.append(sp_t)
    
    facade_face=[]
    facade_other1=[]
    facade_other2=[]
    facade_other3=[]
    facade_other4=[]
    facade_other5=[]
    facade_other6=[]
    facade_other7=[]
    facade_other8=[]
    
    #time_face=[]
    #time_other=[]
    for i in range(len(direction_set)):
        if direction_set[i]==0:
            facade_face.append(data[i])
        elif direction_set[i]==1:
            facade_other1.append(data[i])
        elif direction_set[i]==2:
            facade_other2.append(data[i])
        elif direction_set[i]==3:
            facade_other3.append(data[i])
        elif direction_set[i]==4:
            facade_other4.append(data[i])
        elif direction_set[i]==5:
            facade_other5.append(data[i])
        elif direction_set[i]==6:
            facade_other6.append(data[i])
        elif direction_set[i]==7:
            facade_other7.append(data[i])
        elif direction_set[i]==8:
            facade_other8.append(data[i])
    
    #    if time_set[i]==0:
    #        time_face.append(data[i])
    #    else:
    #        time_other.append(data[i])
    
    first0.write_data(facade_face,savepath+'\\facade_face.txt')
    first0.write_data(facade_other1,savepath+'\\facade_other1.txt')
    first0.write_data(facade_other2,savepath+'\\facade_other2.txt')
    first0.write_data(facade_other3,savepath+'\\facade_other3.txt')
    first0.write_data(facade_other4,savepath+'\\facade_other4.txt')
    first0.write_data(facade_other5,savepath+'\\facade_other5.txt')
    first0.write_data(facade_other6,savepath+'\\facade_other6.txt')
    first0.write_data(facade_other7,savepath+'\\facade_other7.txt')
    first0.write_data(facade_other8,savepath+'\\facade_other8.txt')
#-----------------------piliang--------------------------------

# for i in range(4,5):
#     print (i)
#     filename=r'D:\PCL_DATA\example'+'\\'+'1_00000'+str(i)+'.txt'
#     savepath=r'D:\PCL_DATA\example\sph\\1_00000'+str(i)+'3_sph'
#     create(filename,savepath)
# filename=r"D:\PCL_DATA\dataset_demf\dbld-2\\domfountain_station3_xyz_intensity_rgb - Cloud.txt"
# savepath=r'D:\PCL_DATA\dataset_demf\dbld-2'

filename=r"../example/original_facade_01.txt"
savepath=r'../example/windowframe/'
create(filename,savepath)







