#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Motor torque calculator
Copyright Shokara Inc. 2017
"""

import math
from pylab import *
import pdb
import numpy as np

# preset parameter
Y2 = 1 # [m]
Wtotal = 60 #[kg]
rate = 0.82 # rate of weight over the knees
W = Wtotal*rate
g = 9.8 # gravity
m1 = 1 # [kg]
m2 = 1 # [kg]
w1 = 1 # [kg]
w2 = 1 # [kg]

def inverse_kinematics(theta1,theta2):
    theta3 = theta1+theta2 - pi
    x0 = [0,0]
    if theta1>=pi/2:
        x1 = [-abs(L1*cos(pi-theta1)),L1*sin(pi-theta1)]
    else:
        x1 = [abs(L1*cos(pi-theta1)),L1*sin(pi-theta1)]

    x2 = [x1[0]+L2*cos(theta3),x1[1]+L2*sin(theta3)]
    show_stick(x0,x1,x2)

def show_stick(x0,x1,x2):
    circle(x0)
    circle(x1)
    line(x0,x1)
    line(x1,x2)
    show() 

def circle(xc):
    r = 0.02;
    ang=linspace(0,2*pi,20)
    xp=[r*cos(a) for a in ang]
    yp=[r*sin(a) for a in ang]
    xcp = [xc[0] + x for x in xp]
    ycp = [xc[1] + y for y in yp]
    plot(xcp,ycp,"r",linewidth=2);
    axis('equal')

def line(x0,x1):
    xs = linspace(x0[0],x1[0],10);
    ys = linspace(x0[1],x1[1],10);
    plot(xs,ys,"b",linewidth=2);


def compute(x, y):
    """arguments: x:X2, y:Y2"""
    #inverse kinematics
    cos_a = (-(x**2+y**2)+L1**2+L2**2)/(2*L1*L2)
    a = - math.atan2(sqrt(1 - cos_a**2), cos_a)
    theta2 = - a
    theta2_dash = pi - a
    theta1 = math.atan2(x, y) \
               - math.atan2(L2*sin(theta2_dash), L1+L2*cos(theta2_dash))
    #calculate motor torque M2
    alpha = math.atan2(380,600)
    F = W*g*sin(alpha)
    theta3 = theta1+theta2-pi
    gamma = alpha + theta3 - pi/2
    M2 = 0.5*L2*m2*g*cos(theta3) + F*L2*cos(gamma)
    #calculate motor torque M1
    L3 = L1**2 + (L2/2)**2 - 2*L1*(L2/2)*cos(theta2) # The therom of cosines
    L4 = L1**2 + L2**2 - 2*L1*L2*cos(theta2)
    try: 
        alpha1 = math.acos((L1**2+L3**2-(L2/2)**2)/(2*L1*L3))
    except Exception:
        return
    alpha2 = pi - (theta3+alpha1)
    theta4 = pi/2 - alpha2
    try:
        theta5 = math.acos((L2**2+L4**2-L1**2)/(2*L2*L4))
    except  Exception:
        return

    M1 = m2*g*cos(theta4)*L3 + F*cos(gamma)*cos(theta5)*L4 \
            - 0.5*m1*g*L1*sin(theta1) - w2*g*L1*sin(theta1)
    if(math.isnan(M1) or math.isnan(M2)):
        return

    print(theta1*180/pi,theta2*180/pi)
    inverse_kinematics(theta1,theta2)
    return (M1, M2)

inverse_kinematics(50*pi/180,50*pi/180)
exit()

X2s = linspace(-0.3,0.3,7)
L1s = linspace(0.3, 1.5, 10)
L2s = linspace(0.3, 1.5, 10)

M1s = []
M2s = []
params = []
for X2 in X2s:
    for L1 in L1s:
        for L2 in L2s:
            result = compute(X2,Y2)
            if result!=None:
                M1s.append(abs(result[0]))
                M2s.append(abs(result[1]))
                params.append((X2,L1,L2))
        
i1 = M1s.index(max(M1s))
print("max M1: ", max(M1s))
print("X2: ", params[i1][0], ", L1: ", params[i1][1], ", L2: ", params[i1][2])
print()

i2 = M2s.index(max(M2s))
print("max M2: ", max(M2s))
print("X2: ", params[i2][0], ", L1: ", params[i2][1], ", L2: ", params[i2][2])

