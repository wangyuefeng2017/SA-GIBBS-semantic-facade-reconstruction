# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:06:46 2020

@author: wyf-laptop
"""

import numpy as np
import copy

def generate_v(para_set_old,range_faca): # randomly produce the vertexes in graph.
    para_set_new=copy.copy(para_set_old)
    nwindow=para_set_new['nwindow']
    
    leave_window=int(nwindow/2)
    # n_vert=int(nwindow-2)
    # if n_vert>1:
    #     nv=np.random.randint(1,n_vert) #para_set_new['num_vertices'] 
    # else:
    #     nv=1
    
    nv=para_set_new['num_vertices']
    para_set_new['num_eachwindow']={}
    print (nwindow, nv)
    if para_set_new['mode']=='sysm' and nwindow%2==0 and nv>1:
        
        if nv%2==0: # if the number of vertexes is even, assigning elements to each vertex
            for ne in range(int(nv/2)):
                if ne!=int(nv/2)-1 and leave_window-int(nv/2)+ne>1:
                    para_set_new['num_eachwindow'][str(ne)]=np.random.randint(1,leave_window-int(nv/2)+ne+1)
                    para_set_new['num_eachwindow'][str(nv-1-ne)]=para_set_new['num_eachwindow'][str(ne)]
                    leave_window-=para_set_new['num_eachwindow'][str(ne)]
                else:
                    para_set_new['num_eachwindow'][str(ne)]=leave_window
                    para_set_new['num_eachwindow'][str(nv-1-ne)]=para_set_new['num_eachwindow'][str(ne)]
        else: # if the number of vertexes is odd, assigning elements to each vertex
            for ne in range(int(nv/2)):
                if leave_window-int(nv/2)+ne>1:
                    print (leave_window-int(nv/2)+ne)
                    para_set_new['num_eachwindow'][str(ne)]=np.random.randint(1,leave_window-int(nv/2)+ne+1)
                    para_set_new['num_eachwindow'][str(nv-1-ne)]=para_set_new['num_eachwindow'][str(ne)]
                    leave_window-=para_set_new['num_eachwindow'][str(ne)]
                else:
                    para_set_new['num_eachwindow'][str(ne)]=1
                    para_set_new['num_eachwindow'][str(nv-1-ne)]=1
                    
            para_set_new['num_eachwindow'][str(int(nv/2))]=np.int(2*leave_window)
            
    elif para_set_new['mode']=='sysm' and nwindow%2==1 and nv>1:
        if nv%2==0:
            nv-=1
            para_set_new['num_vertices']=nv
        for ne in range(int(nv/2)):
            if leave_window-int(nv/2)+ne==1:
                para_set_new['num_eachwindow'][str(ne)]=1
                para_set_new['num_eachwindow'][str(nv-1-ne)]=1
                leave_window-=1#leave_window-2
            else:
                if leave_window-int(nv/2)+ne>1:
                    para_set_new['num_eachwindow'][str(ne)]=np.random.randint(1,leave_window-int(nv/2)+ne+1)
                    para_set_new['num_eachwindow'][str(nv-1-ne)]=para_set_new['num_eachwindow'][str(ne)]
                    leave_window-=para_set_new['num_eachwindow'][str(ne)]
                else:
                    para_set_new['num_eachwindow'][str(ne)]=1
                    para_set_new['num_eachwindow'][str(nv-1-ne)]=1
                    leave_window-=para_set_new['num_eachwindow'][str(ne)]
        para_set_new['num_eachwindow'][str(int(nv/2))]=np.int(2*leave_window)+1
    
    elif para_set_new['mode']=='sysm' and nv==1:
        para_set_new['num_eachwindow']={'0':nwindow}
        
    elif para_set_new['mode']=='asysm' and nwindow>=3:
        # print (nwindow)
        # para_set_new['num_vertices']=2
        para_set_new['num_eachwindow']['0']=np.random.randint(1,nwindow)
        para_set_new['num_eachwindow']['1']=nwindow-para_set_new['num_eachwindow'][str(0)]

    return para_set_new

def generate_edge(W,H,para_set_old,range_faca):# randomly produce the edges in graph according the vertexes.
    theta_new=copy.copy(para_set_old)
    dict_inter={}
    dict_intra={}
    nv=theta_new['num_vertices']
    nwindow=theta_new['nwindow']
    leave_width=W-theta_new['w_window']*nwindow#-theta_new['w_bound']  #两侧空间
    each_edge=leave_width/(nwindow-1)
    
    if theta_new['num_eachwindow']['0']>1:
        d_intra=round(np.random.uniform(range_faca['w_sp'][0],min(3,each_edge)),1)
        d_use=d_intra*(theta_new['num_eachwindow']['0']-1)
        dict_intra['0']=d_intra
    else:
        d_intra=0
        dict_intra['0']=d_intra
        d_use=0
    
    if theta_new['mode']=='sysm' and nv%2==0 and nv>2:
        dict_intra[str(2*nv-2)]=d_intra
        d_use+=d_intra*(theta_new['num_eachwindow']['0']-1)
        dict_inter[str(int((2*nv-3)/2)+1)]=round(np.random.uniform(each_edge,min(3,2*each_edge+theta_new['w_window'],(leave_width-d_use)/2)),2)
        d_use+=dict_inter[str(int((2*nv-3)/2)+1)]
        for dx in range(int((2*nv-3)/2)):
            if dx%2==0:
                d_inter=round(np.random.uniform(each_edge,min(3,2*each_edge+theta_new['w_window'],(leave_width-d_use)/2)),2)
                d_use+=2*d_inter
                dict_inter[str(dx+1)]=d_inter
                dict_inter[str(2*nv-2-dx-1)]=d_inter
            else:
                if theta_new['num_eachwindow'][str(int((dx+1)/2))]==1:
                    dict_intra[str(dx+1)]=0
                    dict_intra[str(2*nv-2-dx-1)]=0
                else:
                    d_intra=round(np.random.uniform(range_faca['w_sp'][0],min(3,each_edge,(leave_width-d_use)/2)),2)
                    d_use+=2*d_intra*(theta_new['num_eachwindow'][str(int((dx+1)/2))]-1)
                    dict_intra[str(dx+1)]=d_intra
                    dict_intra[str(2*nv-2-dx-1)]=d_intra
            # print (dx)
        
        
    elif theta_new['mode']=='sysm' and nv==2:
    
        dict_intra[str(2*nv-2)]=d_intra
        dict_inter['1']=round(leave_width-d_use*2,2)
    
    elif theta_new['mode']=='sysm' and nv%2==1 and nv>1:
        dict_intra[str(2*nv-2)]=d_intra
        d_use+=d_intra*(theta_new['num_eachwindow']['0']-1)
        dict_intra[str(int((2*nv-3)/2)+1)]=round(np.random.uniform(range_faca['w_sp'][0],min(3,each_edge,(leave_width-d_use)/2)),2)
        dict_intra[str(int((2*nv-3)/2)+1)]*(theta_new['num_eachwindow'][str(int((nv-1)/2))]-1)
        
        for dx in range(int((2*nv-3)/2)):
            if dx%2==0:
                d_inter=round(np.random.uniform(each_edge,min(3,2*each_edge+theta_new['w_window'],(leave_width-d_use)/2)),2)
                d_use+=2*d_inter
                dict_inter[str(dx+1)]=d_inter
                dict_inter[str(2*nv-2-dx-1)]=d_inter
            else:
                if theta_new['num_eachwindow'][str(int((dx+1)/2))]==1:
                    dict_intra[str(dx+1)]=0
                    dict_intra[str(2*nv-2-dx-1)]=0
                else:
                    d_intra=round(np.random.uniform(range_faca['w_sp'][0],min(3,each_edge,(leave_width-d_use)/2)),2)
                    d_use+=2*d_intra*(theta_new['num_eachwindow'][str(int((dx+1)/2))]-1)
                    dict_intra[str(dx+1)]=d_intra
                    dict_intra[str(2*nv-2-dx-1)]=d_intra  
    elif theta_new['mode']=='sysm' and nv==1:
        d_intra=each_edge
        dict_intra['0']=d_intra


    elif theta_new['mode']=='asysm' and nv==2:
    
        d_intra2=round(np.random.uniform(range_faca['w_sp'][0],max(0.2,min(3,each_edge,leave_width-d_use))),2)
        d_use+=d_intra2*(theta_new['num_eachwindow']['1']-1)
        dict_intra[str(2*nv-2)]=d_intra2
        dict_inter['1']=round(leave_width-d_use,2)
    
    theta_new['edge']={'d_intra':dict_intra,
                       'd_inter':dict_inter}
    
    return theta_new['edge']

def gibbs(W,H,para_set,i,range_para,va): 
    para_set_new=copy.copy(para_set)
    para_i=list(para_set_new.keys())[i]
    # print (para_i)
    if para_i=='nwindow':
        nwindow_min=max(range_para['nwindow'][0],int((W-para_set_new['w_bound'])/(para_set_new['w_window']+range_para['w_sp'][1])))  #space range (0.2,3)
        nwindow_max=max(nwindow_min+1,min(range_para['nwindow'][1],int((W-para_set_new['w_bound'])/(para_set_new['w_window']+range_para['w_sp'][0]))))
        if para_set_new['mode']=='asysm' and nwindow_max>3:
            nwindow=np.random.randint(3,nwindow_max+1)
            para_set_new['nwindow']=nwindow
        else:
            nwindow=np.random.randint(nwindow_min,nwindow_max+1)
            para_set_new['nwindow']=nwindow
        
        if va>0.4:
            para_set_new2=generate_v(para_set_new, range_para)
            para_set_new['num_eachwindow']=para_set_new2['num_eachwindow']
            para_set_new['num_vertices']=para_set_new2['num_vertices']
            para_set_new['edge']=generate_edge(W, H, para_set_new2, range_para)
        else:
            para_set_new['num_vertices']=1
            para_set_new['num_eachwindow']={'0':nwindow}
            para_set_new['edge']={'d_intra':{'0':0},
                                  'd_inter':{}}
            
    elif para_i=='h_roof':
        para_set_new['h_roof']=round(np.random.uniform(range_para['h_roof'][0],range_para['h_roof'][1]),2)
        # para_set_new['h_first']=round(np.random.uniform(3.5,6.5),2)
        leave_h=H-para_set_new['h_roof']-para_set_new['h_first']
        nfloor_min=int(leave_h/range_para['h_floor'][1])+1
        nfloor_max=int(leave_h/range_para['h_floor'][0])
        # if int(leave_h/range_para['h_floor'][0])==0:
        #     para_set_new['h_floor']=0
        if nfloor_min<nfloor_max:
            nfloor=np.random.randint(nfloor_min,nfloor_max+1)
            para_set_new['h_floor']=round(leave_h/float(nfloor),2)
        else:
            para_set_new['h_floor']=round(leave_h/float(nfloor_min),2)
     
    elif para_i=='h_first':
        # para_set_new['h_roof']=round(np.random.uniform(0,1.5),2)
        para_set_new['h_first']=round(np.random.uniform(range_para['h_first'][0],range_para['h_first'][1]),2)
        leave_h=H-para_set_new['h_roof']-para_set_new['h_first']
        nfloor_min=int(leave_h/range_para['h_floor'][1])+1
        nfloor_max=int(leave_h/range_para['h_floor'][0])
        if nfloor_min<nfloor_max:
            nfloor=np.random.randint(nfloor_min,nfloor_max+1)
            para_set_new['h_floor']=round(leave_h/float(nfloor),2)
        else:
            para_set_new['h_floor']=round(leave_h/float(nfloor_min),2)
    
    elif para_i=='h_floor':
        leave_h=H-para_set_new['h_roof']-para_set_new['h_first']
        nfloor_min=int(leave_h/range_para['h_floor'][1])+1
        nfloor_max=int(leave_h/range_para['h_floor'][0])
        if nfloor_min<nfloor_max:
            nfloor=np.random.randint(nfloor_min,nfloor_max+1)
            para_set_new['h_floor']=round(leave_h/float(nfloor),2)
        else:
            para_set_new['h_floor']=round(leave_h/float(nfloor_min),2)
            
    elif para_i=='h_gap':
        h_floor=para_set_new['h_floor']
        h_window=para_set_new['h_window']
        leave_h=h_floor-h_window
        para_set_new[para_i]=round(np.random.uniform(0,leave_h),2)
        
    elif para_i=='h_fgap':
        h_first=para_set_new['h_first']
        h_window=para_set_new['h_window']
        leave_h=h_first-h_window
        para_set_new[para_i]=round(np.random.uniform(0,leave_h),2)
        
    elif para_i=='h_window':
        h_floor=para_set_new['h_floor']
        h_gap=para_set_new['h_gap']
        leave_h=h_floor-h_gap
        para_set_new[para_i]=round(np.random.uniform(range_para['h_window'][0],min(range_para['h_window'][1],leave_h-0.1)),2)
        
    elif para_i=='w_window':
        w_b=para_set_new['w_bound']
        
        leave_width=(W-w_b)/float(para_set_new['nwindow']-1)
        para_set_new[para_i]=round(np.random.uniform(range_para['w_window'][0],max(range_para['w_window'][0],min(range_para['w_window'][1],leave_width-range_para['w_sp'][0]))),2)
        if va>0.4:
            para_set_new2=generate_v(para_set_new, range_para)
            para_set_new['num_eachwindow']=para_set_new2['num_eachwindow']
            para_set_new['num_vertices']=para_set_new2['num_vertices']
            para_set_new['edge']=generate_edge(W, H, para_set_new, range_para)

    elif para_i=='w_bound':
        if va<=0.4:
            para_set_new[para_i]=round(np.random.uniform(range_para['w_bound'][0],range_para['w_bound'][1]),2)
        else:
            amount_e=0
            for i in range(len(para_set_new['edge']['d_intra'])):
                amount_e+=para_set_new['edge']['d_intra'][str(2*i)]*(para_set_new['num_eachwindow'][str(i)]-1)
            
            for i in range(len(para_set_new['edge']['d_inter'])):
                amount_e+=para_set_new['edge']['d_inter'][str(2*i+1)]
            
            para_set_new[para_i]=W-amount_e-para_set_new['nwindow']*para_set_new['w_window']

    elif  para_i=='num_eachwindow':
        para_set_new2=generate_v(para_set_new, range_para)
        para_set_new['num_eachwindow']=para_set_new2['num_eachwindow']
        para_set_new['num_vertices']=para_set_new2['num_vertices']
        para_set_new['edge']=generate_edge(W, H, para_set_new, range_para)
    
    elif  para_i=='num_vertices':
        nwindow=para_set_new['nwindow']
        n_vert=int(nwindow-2)
        if n_vert>1:
            nv=np.random.randint(1,n_vert+1) #para_set_new['num_vertices'] 
        else:
            nv=1
        
        if para_set_new['mode']=='sysm' and nwindow%2==1 and nv%2==0:
            nv-=1
        
        elif para_set_new['mode']=='asysm' and nwindow>=3:
            nv=2
        
        para_set_new['num_vertices']=nv
        para_set_new2=generate_v(para_set_new, range_para)
        para_set_new['num_eachwindow']=para_set_new2['num_eachwindow']
        para_set_new['num_vertices']=para_set_new2['num_vertices']
        para_set_new['edge']=generate_edge(W, H, para_set_new, range_para)
        
    elif  para_i=='edge':
        para_set_new['edge']=generate_edge(W, H, para_set_new, range_para)
    
    elif para_i=='mode':
        if para_set_new['mode']=='sysm' and para_set_new['nwindow']>3:
            para_set_new['mode']='sysm'
        else:
            para_set_new['mode']='sysm'
            
        para_set_new2=generate_v(para_set_new, range_para)
        para_set_new['num_eachwindow']=para_set_new2['num_eachwindow']
        para_set_new['num_vertices']=para_set_new2['num_vertices']
        para_set_new['edge']=generate_edge(W, H, para_set_new, range_para)
        
    return para_set_new