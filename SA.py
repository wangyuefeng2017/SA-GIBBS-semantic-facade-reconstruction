# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:22:11 2020

@author: wyf-laptop
"""

import numpy as np
import random
import matplotlib.pyplot as plt 
import copy
import math
import getrect
import prior
import likelihood
import sampling

def plot_result(x_new,y_new,point_window,rect_window,xmin,ymin,amd):
    # fig = plt.figure()
    
    fig=plt.figure(dpi=120)
    ax = fig.add_subplot(111)
    plt.scatter(x_new,y_new,c='b',marker='.',s=2,linewidth=0,alpha=1,cmap='spectral')
    plt.title(str(amd)+'--Posterior Distribution Simulated Annealing');
    for k in point_window.keys():
        if point_window[k] !=[]:
            plt.scatter(point_window[k][0],point_window[k][1],marker='.',s=2,linewidth=0,alpha=1,cmap='spectral')
            # plt.hold
      
    plt.xlim(min(x_new)-1,max(x_new)+2)
    plt.ylim(min(y_new)-1,max(y_new)+2)

    for i in range(len(rect_window)):
        (x,y),w,h=rect_window[i]
        rect1=plt.Rectangle((x+xmin,y+ymin),w,h,color='red',fill=False)
        ax.add_patch(rect1)

    plt.show()

def choose_stage(prev_posterior,i,iterations):
    
    if prev_posterior<=0.5 and  i/iterations<0.3333: #prev_posterior<0.5 or 
        a=0.8;b=0.1;c=0.1
    elif prev_posterior<=0.5 and  i/iterations>=0.3333: #prev_posterior<0.5 or 
        a=0.6;b=0.3;c=0.1 
        
    elif 0.5<=prev_posterior<=0.7 and 0.3333<=i/iterations<0.888: #0.5<=prev_posterior<0.7 or 
        a=0.1;b=0.8;c=0.1
    
    elif 0.5<=prev_posterior<=0.7 and i/iterations>=0.888: #0.5<=prev_posterior<0.7 or 
        a=0.1;b=0.6;c=0.3
        
    elif prev_posterior>=0.7 and 0.888<=i/iterations<=1: #prev_posterior>=0.7 or 
        a=0.1;b=0.1;c=0.8
        
    else:
        a=0.4;b=0.3;c=0.3
    
    stage=np.random.choice(['st1','st2','st3'],p=[a,b,c])
    if stage=='st1':
        stagen=0; various=8
    elif stage=='st2':
        stagen=6; various=12
    elif stage=='st3':
        stagen=11; various=12
    else:
        stagen=0;various=8

    return stagen,various
    
#----------------------implement------------------

def simulated_annealing(W,H,xmin,ymin,iterations,x_new,y_new, theta, range_faca):
    
    guessed = [];
    accepted = [];
    accepted.append(theta)
    best_post=[]
    post=[]
    post2=[]
    priorscore=[]
    likeli=[]
    p_windows= getrect.window_rect(W,H,theta);
    prev_posterior = prior.score_fuc_vertfied_layout(W,H,theta) * likelihood.score_fuc_likelihood(xmin,ymin,theta,x_new,y_new,p_windows)[0];
    best_post.append(prev_posterior)
    accumulation=0
    various=8
    stagen=0
    amd=0
    for i in range(0,iterations):
        print('SA', i/iterations, best_post[-1], prev_posterior, prior.score_fuc_vertfied_layout(W,H,theta), likelihood.score_fuc_likelihood(xmin,ymin,theta,x_new,y_new,p_windows)[0]);
        for j in range(10):
            theta_i=stagen
            print ('stage',theta_i,various)
            while theta_i<various:
                amd+=1
                theta_guess = sampling.gibbs(W,H,theta,theta_i, range_faca, prev_posterior);
                guessed.append(theta_guess);
                p_windows= getrect.window_rect(W,H,theta_guess)
                pr=prior.score_fuc_vertfied_layout(W,H,theta_guess)
                # lh=1-likelihood.score_fuc_likelihood(xmin,ymin,theta_guess,x_new,y_new,p_windows)[0] # for low-quality data, llow=1-l(D|theta)
                lh=likelihood.score_fuc_likelihood(xmin,ymin,theta_guess,x_new,y_new,p_windows)[0] # for refinement of facade structure
                new_posterior = pr*lh; 
                if new_posterior>0:
                    post2.append(new_posterior)
                if pr!=0:
                    priorscore.append(pr)
                likeli.append(lh)
                #compute change in energy from previous state
                d_E = new_posterior - prev_posterior;
                #create annealing schedule
                T = iterations*0.85**(20+i)#ffloat(iterations - i) * 10**(-5);#
                # as time increases, probability of accepting smaller values decreases
                if (d_E > 0) or (math.exp(d_E/T) > random.random()):
                    accumulation=0
                    theta = copy.copy(theta_guess);
                    prev_posterior = new_posterior;
                    if new_posterior>best_post[-1]:
                        accepted.append(theta);
                        best_post.append(new_posterior)
                    # print (theta,d_E)
                        p_window=getrect.window_rect(W,H,theta)
                        point_window=likelihood.score_fuc_likelihood(xmin,ymin,theta,x_new,y_new,p_window)[1]
                        plot_result(x_new,y_new,point_window,p_window,xmin,ymin,amd)
                        print (theta, theta_i)
                else:
                    # print ('theta_guess',theta_guess)
                    accumulation+=1
                    # print (accumulation,i)
                theta_i+=1
                if prev_posterior>0:
                    post.append(1-prev_posterior)
                best_post.append(best_post[-1])
            
            # stagen=0
            # various=8
            # theta=accepted[-1]
        stagen,various=choose_stage(prev_posterior,i,iterations)
        if accumulation>1500 or T<10**(-6):
            print ('end', i,  accumulation)
            # break
        theta = copy.copy(accepted[-1])
    print('Simulated Annealing', len(accepted), len(guessed),len(post),len(post2));
    plt.figure(2);
    plt.title('Posterior Distribution w/ Simulated Annealing');
    plt.plot(best_post, color='r', mfc='w',label='uniprot90_train');
    plt.figure(3);
    plt.title('Posterior Distribution2 w/ Simulated Annealing');
    plt.plot(post2, color='g',label='uniprot90_test');
    plt.figure(4);
    plt.title('Prior w/ Simulated Annealing');
    plt.plot(priorscore, color='b',label='uniprot90_test');
    plt.figure(5);
    plt.title('Likelihood w/ Simulated Annealing');
    plt.plot(likeli, color='c',label='uniprot90_test');   
    plt.figure(6);
    plt.title('Likelihood w/ Simulated Annealing');
    plt.plot(post, color='c',label='uniprot90_test');
    
    return accepted,guessed,post