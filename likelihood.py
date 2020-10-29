# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:21:07 2020

@author: wyf-laptop
"""
import numpy as np

def score_fuc_likelihood(xmin,ymin,para_set,x_new,y_new,p_windows):  #x_new,y_new分别位点云转换后的坐标；p_window=((x,y),w,h)
    window_center_pc=[]   # the geometrics centre of each window
    for i in range(len(p_windows)):
        window_center_pc.append((p_windows[i][0][0]+p_windows[i][1]/2+xmin,p_windows[i][0][1]+p_windows[i][2]/2+ymin))
    
    point_window={}  # each window with special pointcloud
    point_sum=0   # the amount of used point
    #    point_area={}
    for x,y in window_center_pc:
        point_save_x=[]
        point_save_y=[] # xp,yp are the scope of windows in pointcloud
        xpmax,xpmin,ypmax,ypmin=x+para_set['w_window']/2,x-para_set['w_window']/2,y+para_set['h_window']/2,y-para_set['h_window']/2
        n=str(x+y)
        for i in range(len(x_new)):
            if xpmin<x_new[i]<xpmax and ypmin<y_new[i]<ypmax:
                point_save_x.append(x_new[i])
                point_save_y.append(y_new[i])
                point_sum+=1
                
        point_window[n]=[point_save_x,point_save_y]
        
    score1=point_sum/np.float(len(x_new))
    #    print score1
    r=500
    if para_set['w_window']*para_set['h_window']*len(p_windows)==0:
        print (para_set)
    if len(p_windows)>0:
        score21=point_sum/np.float(r*(para_set['w_window']*para_set['h_window']*len(p_windows)))
    else:
        score21=0
    #roof 密度越大越好

    return (0.5*score1+0.5*score21),point_window  # 越接近1越好  