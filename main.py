# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:30:31 2020

@author: wyf-laptop
"""

import matplotlib.pyplot as plt 
import copy
import likelihood
import transfer2D
import SA
import getrect

def plot_all(opt_para,p_window,W,H,xmin,ymin):
    fig=plt.figure(dpi=120)
    ax = fig.add_subplot(111)
    # plt.scatter(x_new,y_new,c='r',marker='.',s=2,linewidth=0,alpha=1,cmap='spectral')
    plt.title('--heirarchy');

    yroof=H-opt_para['h_roof']
    rect1=plt.Rectangle((xmin,yroof+ymin),W,opt_para['h_roof'],color='red')
    ax.add_patch(rect1)
    
    nfloor=int((H-opt_para['h_roof']-opt_para['h_first'])/opt_para['h_floor'])
    for i in range(nfloor):
        yfloor=H-opt_para['h_roof']-(i+1)*opt_para['h_floor']
        rect1=plt.Rectangle((xmin,yfloor+ymin),W,opt_para['h_floor'],color='yellow')
        ax.add_patch(rect1)
    # yfground=0
    rect1=plt.Rectangle((xmin,ymin),W,opt_para['h_first'],color='green')
    ax.add_patch(rect1)
    for (x,y),w,h in p_window:
        rect1=plt.Rectangle((x+xmin,y+ymin),w,h,color='blue')
        ax.add_patch(rect1)
    
    # plt.xlim(xmin-1,xmin+W+2)
    # plt.ylim(ymin-1,ymin+H+2)
    ax.set_xlim(xmin-1,xmin+W+2)
    ax.set_ylim(ymin-1,ymin+H+2)
    ax.set_aspect(1)
    plt.show()  


if __name__ == '__main__':
    filename=r"example/face1.txt"
    
    x_new,y_new=transfer2D.getplane_new(filename)
    
    xmax=max(x_new)
    xmin=min(x_new)
    ymax=max(y_new)
    ymin=min(y_new)
    
    W=xmax-xmin
    H=ymax-ymin
    
    range_faca={'nwindow':(2,W/(1.5)+1),
                'h_floor':(3,5),
                'h_first':(3,5),
                'h_roof':(0.0,1),
                'h_gap':(0.0,2.5),
                'h_fgap':(0.0,2.5),
                'h_window':(1.0,2.6),
                'w_window':(0.5,2.5),
                'w_sp':(0.5,2.0),
                'w_bound':(0.1,3.5)}
    
    para_set_init={'h_floor':3.5111,
                    'h_first':3.0,
                    'h_roof':1.6,
                    'h_gap':1.0,
                    'h_fgap':1,
                    'h_window':1.0,
                    'w_bound':0.8,
                    'w_window':1.2,
                    'nwindow':8,
                    'mode':'sysm',
                    'num_vertices':1,
                    'num_eachwindow':{'0':8},
                    'edge':{'d_intra':{'0':0},
                            'd_inter':{}
                            }
                    }
    # range_faca=getrange_para(W,H,para_set_init)
    para_set=copy.copy(para_set_init)
    iterations=100
    
    
    accepted,guessed,post=SA.simulated_annealing(W,H,xmin,ymin,iterations, x_new, y_new, para_set_init, range_faca)
    # accepted,accepted_gibbs=metropolis_hastings(iterations,x_new,y_new,para_set_init)
    opt_para=accepted[-1]
    
    p_window=getrect.window_rect(W,H,opt_para)
    point_window=likelihood.score_fuc_likelihood(xmin,ymin,opt_para,x_new,y_new,p_window)[1]
    SA.plot_result(x_new,y_new,point_window,p_window,xmin,ymin,11)
    plot_all(opt_para,p_window,W,H,xmin,ymin)
    
    
    
    
    
    
