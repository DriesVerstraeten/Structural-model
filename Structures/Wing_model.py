#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:08:10 2017

@author: driesverstraeten
"""

#Calculations for the WING MODEL

import Init_Parameters as p
import numpy as np
import matplotlib.pyplot as plt

plt.close()
fig = plt.figure(figsize = (9,3),tight_layout=True)

########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
#CHORD LENGTH AT DIFFERENT SPANWISE LOCATIONS

#def wing_parameters(b, MTOW, rho, V, S):
dy = 0.01 #small spanwise section

r2 = .95
r3 = .8
r4 = .4

def ChordBase(r2,r3,r4,b,S):

    return S/((r4/2.0+r3+r2+.5)*(b/3.0))

def GetChords(r2,r3,r4,b,S):

    C1 = ChordBase(r2,r3,r4,b,S)
    C2 = C1*r2
    C3 = C1*r3
    C4 = C1*r4

    return C1,C2,C3,C4


C1,C2,C3,C4 = GetChords(r2,r3,r4,p.b,p.S)

bsection = p.b/6.

c_1 = np.linspace(C1, C2, bsection*1./dy)
c_2 = np.linspace(C2, C3, bsection*1./dy)
c_3 = np.linspace(C3, C4, bsection*1./dy)
c = np.hstack((c_1,c_2,c_3))

y = np.linspace(0,p.b/2.+dy, len(c)) #spanwise location of section
y1 = np.linspace(0,p.b/2.+2*dy, len(c))
#d_cLE = np.tan(p.theta_LE) * y #LE section "to be cut away from chord"
#d_cTE = np.tan(p.theta_TE) * y #TE section "to be cut away from chord"
    
#c = p.c_r - d_cLE - d_cTE #chord at each spanwise section
    

CL = 12 * p.g * p.MTOW / (0.5 * p.rho_0 * p.V_cruise**2. * p.S) #lift coefficient at N g
#CL_45g = p.Nz * p.g * p.MTOW / (0.5 * p.rho_0 * p.V_cruise**2. * p.S) #Lift coefficient at -4.5g
    
                      
########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
#SHEAR AT 9G


def wing_shear(CL, rho, V):
    dL = CL * 1./2. * rho * V**2. * dy * c #the small lift contribution from every section                      
    dL_total = np.zeros(len(y)) #make a list of zeroes to later overwrite these in the next loop
              
    for i in range(0,len(y)):
        if i == 0:
            dL_total[i] = sum(CL * 1./2. * rho * V**2. * dy * c) #overwrite the zeroes
        elif i == 1:
            dL_total[i] = dL_total[i-1] - dL[0]
        else:
            dL_total[i] = dL_total[i-1] - dL[i-1]
    
    ax1 = fig.add_subplot(121)
    ax1.plot(y,dL_total)  
    ax1.set_title('Shear force at -6 g')
    ax1.set_ylabel('Shear force [N]')
    ax1.set_xlabel('Wing span [m]')
    ax1.set_ylim(dL_total[-1],dL_total[0])
    ax1.set_xlim([y[0],y[-1]])
    plt.show()
    
    return dL, dL_total
#print wing_shear(CL, p.rho_0, p.V_cruise)[1][0]
########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
#BENDING AT 9g


def wing_moment(CL, rho, V):
    dM = wing_shear(CL, rho, V)[0] * y
    dM_total = np.zeros(len(y))
    
    for i in range(0,len(y)):
        if i == 0:
            dM_total[i] = sum(dM)
        elif i == 1:
            dM_total[i] = dM_total[i-1] - dM[0]
        else:
            dM_total[i] = dM_total[i-1] - dM[i-1]
    
    ax2 = fig.add_subplot(122)
    ax2.plot(y1,dM_total)  
    ax2.set_title('Bending moment at -6 g')
    ax2.set_ylabel('Bending moment [Nm]')
    ax2.set_xlabel('Wing span [m]')
    ax2.set_ylim(dM_total[-1],dM_total[0])
    ax2.set_xlim([y[0],y[-1]])
    plt.show()
    
    return dM, dM_total

#wing_moment(CL,p.rho_0,p.V_cruise)[1][0]



'''
########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
#BENDING AT -4.5g

def wing_shear_45g(CL, rho, V):
    dL_45g = CL * 1./2. * rho * V**2. * dy * c #the small lift contribution from every section
    dL_45g_total = np.zeros(len(y)+1) #make a list of zeroes to later overwrite these in the next loop
              
    for i in range(0,len(y)+1):
        if i == 0:
            dL_45g_total[i] = sum(CL * 1./2. * rho * V**2. * dy * c) #overwrite the zeroes
        elif i == 1:
            dL_45g_total[i] = dL_45g_total[i-1] - dL_45g[0]
        else:
            dL_45g_total[i] = dL_45g_total[i-1] - dL_45g[i-1]
    
    ax3 = fig.add_subplot(223)
    ax3.plot(y1,dL_45g_total)  
    ax3.set_title('Shear force at -4.5g')
    ax3.set_ylabel('Shear force [N]')
    ax3.set_xlabel('Wing span [m]')
    ax3.set_ylim(dL_45g_total[-1],dL_45g_total[0])
    ax3.set_xlim([y[0],y[-1]])
    plt.show()
    
    return dL_45g, dL_45g_total


########## ########## ########## ########## ########## ########## ########## ########## ########## ##########
#BENDING AT -4.5g


def wing_moment_45g(CL, rho, V):
    dM_45g = wing_shear_45g(CL, rho, V)[0] * y
    dM_45g_total = np.zeros(len(y)+1)
    
    for i in range(0,len(y)+1):
        if i == 0:
            dM_45g_total[i] = sum(dM_45g) #the first point is the total moment
        elif i == 1:
            dM_45g_total[i] = dM_45g_total[i-1] - dM_45g[0] #this is the second point, this is so that the last point is equal to 0
        else:
            dM_45g_total[i] = dM_45g_total[i-1] - dM_45g[i-1] #all the other points
    
    ax4 = fig.add_subplot(224)
    ax4.plot(y1,dM_45g_total)  
    ax4.set_title('Bending moment at -4.5g')
    ax4.set_ylabel('Bending moment [Nm]')
    ax4.set_xlabel('Wing span [m]')
    ax4.set_ylim([dM_45g_total[0],dM_45g_total[-1]])
    ax4.set_xlim([y[0],y[-1]])
    plt.show()
    
    return dM_45g, dM_45g_total

"""
print "Max shear 9g:", wing_shear_9g(CL_9g, p.rho_0, p.V_cruise)[1][0], "N"
print "Max moment 9g:", wing_moment_9g(CL_9g, p.rho_0, p.V_cruise)[1][0], "Nm"
print "Max shear -4.5g:", wing_shear_45g(CL_45g, p.rho_0, p.V_cruise)[1][0], "N"
print "Max moment -4.5g:", wing_moment_45g(CL_45g, p.rho_0, p.V_cruise)[1][0], "Nm"
""" 
'''