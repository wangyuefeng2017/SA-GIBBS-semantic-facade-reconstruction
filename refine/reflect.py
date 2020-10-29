# -*- coding: utf-8 -*-
"""
Created on Sun May  3 19:12:49 2020

@author: wyf-laptop
"""

import os
import first0

"""
According to the reflective of laser points in windows, the window can be extracted.
"""
def ext_win(ii,filename,savepath):
    # ii=72
    # filename=r"example\sph\\window_7_2.txt"
    # savepath=r'example\sph\\'
    data=first0.get_data(filename)
    
    x_set=[]
    y_set=[]
    z_set=[]
    clas_set=[]
    new_data=[]
    for i in range(len(data)):
        if data[i][3]<20:
            new_data.append(data[i])
        x_set.append(data[i][0])
        y_set.append(data[i][1])
        z_set.append(data[i][2])
        clas_set.append(data[i][3])
    
    first0.write_data(new_data,savepath+'window_face_reflect'+'_'+str(ii)+'.txt')


filename=r"../example/original_facade_03.txt"
savepath=r'../example/reflecframe/'

if not os.path.exists(savepath):
        os.makedirs(savepath)
        
ext_win(3,filename,savepath)