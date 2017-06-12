#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:56:43 2017

@author: driesverstraeten
"""
import MOI as mi
import Wing_model as wm
import Init_Parameters as p
import numpy as np
import matplotlib.pyplot as plt
import time 
start_time = time.time()

f1 = mi.wingbox_MOI()[3]
f2 = mi.wingbox_MOI()[4]
y_NA = mi.wingbox_MOI()[5]
x_NA = mi.wingbox_MOI()[6]
x = mi.wingbox_MOI()[7]
x_span1 = mi.wingbox_MOI()[8]
x_span = np.ones(len(x_span1))

    

def wingbox_extreme_pos():
    longest_US = np.sqrt((f1(x)-y_NA)**2 + (x-x_NA)**2)
    longest_LS = np.sqrt((f2(x)-y_NA)**2 + (x-x_NA)**2)

    longest_pos_US = [i for i,p in enumerate(longest_US) if p == np.max(longest_US)]
    longest_pos_LS = [i for i,p in enumerate(longest_LS) if p == np.max(longest_LS)]

    if longest_US[longest_pos_US] > longest_LS[longest_pos_LS]:
        x_location = longest_pos_US
        f = f1
    else: 
        x_location = longest_pos_LS
        f = f2

    return longest_US, longest_LS, x_location, f


for i in range(len(x_span)):
    x_span[i] = x_span1[i][wingbox_extreme_pos()[2]]


def wingbox_bending_stress():
    Mx = wm.wing_moment_9g(wm.CL_9g,p.rho_0,p.V_cruise)[1]
    Ixx = mi.wingbox_MOI()[0]
    Iyy = mi.wingbox_MOI()[1]
    Ixy = mi.wingbox_MOI()[2]
    x_location = wingbox_extreme_pos()[2]
    f = wingbox_extreme_pos()[3]
    
    max_bending_stress = - Mx[0:-1] / (Ixx*Iyy - Ixy**2) * (Iyy*(f(x_span-y_NA) - Ixy*((x_span-x_NA)))) #y_NA changes with the spanwise sections, so change this!!
    max_bending_stressu = - Mx[0:-1] / (Ixx*Iyy - Ixy**2) * (Iyy*(f1(x_span-y_NA) - Ixy*((x_span-x_NA))))
    print max_bending_stress, max_bending_stressu
    
    return max_bending_stress, f

#print wingbox_bending_stress()[0]


plt.plot(wm.y,wingbox_bending_stress()[0])
plt.show()


print("--- %s seconds ---" % (time.time() - start_time))