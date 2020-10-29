# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:17:42 2020

@author: wyf-laptop
"""

def get_data(filename):
    fr = open(filename,'r+')
    
    val_list = fr.readlines()
#    print val_list
    data=[]
    X=[]
    Y=[]
    Z=[]
#    title=val_list[0]
    key_name=val_list[0]
    key_name=key_name.replace('/','')
    key_name=key_name.split(' ')
    
    for value in val_list[2:]:
        value=value.split(' ')
        num=[]
        for n in value:
            num.append(float(n))
        data.append(num)
        X.append(value[0])
        Y.append(value[1])
        Z.append(value[2])
    
    fr.close()
    
    rang_xyz={}
    rang_xyz['x']=[min(X),max(X)]
    rang_xyz['y']=[min(Y),max(Y)]
    rang_xyz['z']=[min(Z),max(Z)]    
    return data

def write_data(data,filename):
    with open(filename,'w') as f:    #设置文件对象
        chardigit='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789. -'
        title='//X Y Z UserData ScanAngleRank NumberOfReturns ReturnNumber GpsTime Intensity Classification'
        f.write(title)
        f.write('\n')
        f.write('100')
        f.write('\n')
        for i in data:
            chs=str(i)
            sts=''
            for ch in chs:
                if ch in chardigit:
                    sts=sts+ch
            f.write(sts)
            f.write('\n')
    f.close()
#filter:caluculate RANSAC
