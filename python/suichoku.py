#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Motor torque calculator
Copyright Shokara Inc. 2017
"""

import math
from pylab import *

# preset parameter
X2 = 0 # VARIABLE [m]
Y2 = 1 # [m]
Wtotal = 60 #[kg]
rate = 0.82 # rate of weight over the knees
W = Wtotal*rate
g = 9.8 # gravity
m1 = 1 # [kg]
m2 = 1 # [kg]
w1 = 1 # [kg]
w2 = 1 # [kg]

def compute(x, y):
    """arguments: x:X2, y:Y2"""
    #inverse kinematics
    cos_a = (-(x**2+y**2)+L1**2+L2**2)/(2*L1*L2)
    try:
        alpha = math.acos(cos_a)
    except Exception:
        return
    theta2 = 2*pi - alpha
    theta1 = math.atan2(x, y) \
               - math.atan2(L2*sin(theta2), L1+L2*cos(theta2))
    #calculate motor torque M2
    F = W*g
    theta3 = theta1+theta2-pi
    gamma = alpha + theta3 - pi/2
    M2 = 0.5*L2*m2*g*cos(theta3) + F*cos(theta3)
    #calculate motor torque M1
    M1 = (W+m2)*g*cos(theta1)*L1 + 0.5*m1*g*L1*sin(theta1)
    return (M1, M2)

L1s = linspace(0.3, 1.5, 10)
L2s = linspace(0.3, 1.5, 10)

M1s = []
M2s = []
for L1 in L1s:
    for L2 in L2s:
        result = compute(X2,Y2)
        if result!=None:
            M1s.append(abs(result[0]))
            M2s.append(abs(result[1]))
        
print("max M1: ", max(M1s), ", max M2: ", max(M2s))

