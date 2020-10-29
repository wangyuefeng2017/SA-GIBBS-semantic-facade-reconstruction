# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:19:28 2020

@author: wyf-laptop
"""
import numpy as np
#-------------score function------------
def vertified_para(W,H,para_set):
    d_inter=para_set['edge']['d_inter']
    d_intra=para_set['edge']['d_intra']
    nwindow=para_set['nwindow']
    w_window=para_set['w_window']
    w_bound=para_set['w_bound']
    mode=para_set['mode']
    num_vertices=para_set['num_vertices']
    num_eachwindow=para_set['num_eachwindow']
    state=[]
    w_id=0
    
    #-----constraint 1:簇内间隔小于相邻节点的簇间间隔-----
    
    if len(list(d_inter.keys()))>0:
        for i in list(d_inter.keys()):
            k=int(i)
            ka=k-1
            kb=k+1
            if d_intra[str(ka)]>d_inter[i] or d_intra[str(kb)]>d_inter[i]:
                state='wrong'      
                w_id=1
                
    #-----constraint 2:所有间隔大于0----
                
            if d_inter[i]<0 or d_intra[str(ka)]<0 or d_intra[str(kb)]<0:
                state='wrong'
                w_id=2
    # elif len(list(d_inter.keys()))==1:
        
    else:
        if d_intra['0']<0:
            state='wrong'
            w_id=3

    #-------constraint3: 边之和必须小于总宽度 ------
    leave_width=W-nwindow*w_window
    amount_e=0
    
    if len(list(para_set['edge']['d_intra'].keys()))==1 or len(list(num_eachwindow.keys()))==1:
        para_set['edge']={'d_intra':{'0':(leave_width-w_bound)/float((nwindow-1))},
                          'd_inter':{}}
        
    for i in range(len(para_set['edge']['d_intra'])):
        amount_e+=para_set['edge']['d_intra'][str(2*i)]*(para_set['num_eachwindow'][str(i)]-1)
    
    for i in range(len(para_set['edge']['d_inter'])):
        amount_e+=para_set['edge']['d_inter'][str(2*i+1)]
        
    wb=(leave_width-amount_e)/2
    if wb<0:
        state='wrong'
        w_id=3
            
    #-------constraint4： 计算得分函数1-------
            
    #-------constraint5：非对称类型窗户个数》2------
            
    if mode=='asysm':
        if nwindow<=2:
            state='wrong'
            w_id=4
    #-------constraint6:若窗户个数为奇数且对称，则节点个数为奇数----
    if nwindow%2==1 and mode=='sysm':
        if num_vertices%2==0:
            state='wrong'
            w_id=5
    
    #-----constraint7: 节点内元素个数和等于总个数------

    #------constraint8: 如果是对称，且节点大于1，则个数要大于3-----
    if mode=='sysm' and num_vertices>1:
        if nwindow<=3:
            state='wrong'
            w_id=8
    #------constraint9: 节点的个数要等于边的个数减1-----

    
    if state!='wrong':
        state='right'
    # print (state,w_id)
    return state

def score_fuc_vertfied_layout(W,H,para_set):
    w_component=0
    area_component=0
    w_windoww=para_set['w_window']
    h_window=para_set['h_window']
    nw=para_set['nwindow']
    h_gap=para_set['h_gap']
    h_fgap=para_set['h_fgap']
    h_floor=para_set['h_floor']
    leave_width=W-nw*w_windoww-para_set['w_bound']
    h_roof=para_set['h_roof'] #round(random.uniform(range_faca['h_roof'][0],range_faca['h_roof'][1]),2)
    h_first=para_set['h_first'] #round(random.uniform(range_faca['h_first'][0],range_faca['h_first'][1]),2)
    num_floor=int((H-h_roof-h_first)/h_floor)+1
    
    state=vertified_para(W,H,para_set)
    w_sp=leave_width/(float(nw))
    if w_sp<0.2:
        value=0
    elif h_gap+h_window>h_floor or h_fgap+h_window>h_first:
        value=0
    elif state=='wrong':
        value=0
    else:
        for i in range(nw):
            w_component+=w_windoww
            area_component+=w_windoww*h_window
            
        r1=w_component/W-(nw/(2*nw-1))   # the ratio of amount width of windows and width of facade
        r2=(area_component*num_floor)/(W*H)-0.3   # # the ratio of amount area of windows and total area of facade
        r3=abs(r1)+abs(r2)
        
        value=abs(np.e**(-r3))
    return  value # 越接近1越好
