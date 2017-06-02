#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:08:10 2017

@author: driesverstraeten
"""

#Calculations for the WING MODEL

import Parameters as p
import numpy as np
import matplotlib.pyplot as plt

plt.close()


########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
#Chord length at different spanwise locations

dy = 0.001 #small spanwise section
y = np.arange(0,p.b/2.+dy, dy) #spanwise location of section
y1 = np.arange(0,p.b/2.+2*dy, dy)
d_cLE = np.tan(p.theta_LE) * y #LE section "to be cut away from chord"
d_cTE = np.tan(p.theta_TE) * y #TE section "to be cut away from chord"

c = p.c_r - d_cLE - d_cTE #chord at each spanwise section

CL_9g = 9. * p.g * p.MTOW / (0.5 * p.rho_0 * p.V_cruise**2. * p.S) #lift coefficient at 9g

                            
########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
#Shear at 9g

dL_9g = CL_9g * 1./2. * p.rho_0 * p.V_cruise**2. * dy * c #the small lift contribution from every section


dL_9g_total = np.zeros(len(y)+1) #make a list of zeroes to later overwrite these in the next loop
          
for i in range(0,len(y)+1):
    if i == 0:
        dL_9g_total[i] = sum(CL_9g * 1./2. * p.rho_0 * p.V_cruise**2. * dy * c) #overwrite the zeroes
    elif i == 1:
        dL_9g_total[i] = dL_9g_total[i-1] - dL_9g[0]
    else:
        dL_9g_total[i] = dL_9g_total[i-1] - dL_9g[i-1]

#plt.plot(y1,dL_9g_total)  


########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
#Bending at 9g

dM_9g = dL_9g * y

dM_9g_total = np.zeros(len(y)+1)

for i in range(0,len(y)+1):
    if i == 0:
        dM_9g_total[i] = sum(dM_9g)
    elif i == 1:
        dM_9g_total[i] = dM_9g_total[i-1] - dM_9g[0]
    else:
        dM_9g_total[i] = dM_9g_total[i-1] - dM_9g[i-1]

plt.plot(y1,dM_9g_total)  

plt.show