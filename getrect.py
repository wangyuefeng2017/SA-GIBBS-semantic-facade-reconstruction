# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:18:01 2020

@author: wyf-laptop
"""
import copy

def window_rect(W,H,para_set_old):
    para_set=copy.copy(para_set_old)
    #   parameters
    nwindow=para_set['nwindow']
    w_bound=para_set['w_bound']
    h_window=para_set['h_window']
    h_roof=para_set['h_roof'] #round(random.uniform(range_faca['h_roof'][0],range_faca['h_roof'][1]),2)
    h_gap=para_set['h_gap'] #round(random.uniform(range_faca['h_gap'][0],range_faca['h_gap'][1]),2)
    h_first=para_set['h_first'] #round(random.uniform(range_faca['h_first'][0],range_faca['h_first'][1]),2)
    h_floor=para_set['h_floor'] #round(random.uniform(range_faca['h_floor'][0],range_faca['h_floor'][1]),2)
    w_window=para_set['w_window']
    leave_width=W-nwindow*para_set['w_window']
    h_fgap=para_set['h_fgap']
    # print (para_set)
    amount_e=0
    if len(list(para_set['edge']['d_intra'].keys()))==1 or len(list(para_set['num_eachwindow'].keys()))==1:
        para_set['edge']={'d_intra':{'0':(leave_width-w_bound)/float((nwindow-1))},
                          'd_inter':{}}
        
    for i in range(len(para_set['edge']['d_intra'])):
        amount_e+=para_set['edge']['d_intra'][str(2*i)]*(para_set['num_eachwindow'][str(i)]-1)
    
    for i in range(len(para_set['edge']['d_inter'])):
        amount_e+=para_set['edge']['d_inter'][str(2*i+1)]
        
    wb=(leave_width-amount_e)/2
    
    
        
    num_floor=int((H-h_roof-h_first)/h_floor)+1
    p_window=[]
    
    for nf in range(1,num_floor): # for each floor, assigning the windows
        h_sp=H-h_roof-h_floor*nf+h_gap
        w_sp=wb
        nv=-1
        nm=0
        para_set['num_eachwindow']['-1']=0
        if para_set['num_vertices']>1:
            for n in range(nwindow): # for each windows, the position need to be calculated
                if nm<n<para_set['num_eachwindow'][str(nv+1)]+nm:
                    w_sp+=w_window+para_set['edge']['d_intra'][str(2*(nv+1))]
                
                elif n==para_set['num_eachwindow'][str(nv+1)]+nm:
                    nm+=para_set['num_eachwindow'][str(nv+1)]
                    w_sp+=para_set['edge']['d_inter'][str(2*(nv+1)+1)]+w_window
                    nv+=1
                p_window.append(((w_sp,h_sp),w_window,h_window))
                
        else:
            for n in range(nwindow):
            # w_sp=wb+para_set['w_window']*nwindow+para_set['edge']['d_intra'][str(2*(nv+1))]
                w_sp=wb+(w_window+para_set['edge']['d_intra'][str(2*(nv+1))])*n
                p_window.append(((w_sp,h_sp),w_window,h_window))
                
        del para_set['num_eachwindow']['-1']
     
    h_sp=h_fgap
    w_sp=(leave_width-w_bound)/float((nwindow-1))
    for nw in range(nwindow): # an uniform distribution can be allocated to ground-floor
        w_x=w_bound/2+(w_window+w_sp)*nw
        p_window.append(((w_x,h_sp),w_window,h_window))    
        
    return p_window