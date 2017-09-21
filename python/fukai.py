#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Motor torque calculator
Copyright Shokara Inc. 2017
"""

import math
from pylab import *

# preset parameter
# L1 = 0.65 # VARIABLE [m]
# L2 = 0.65 # VARIABLE [m]
# X2 = 0.15 # VARIABLE [m]
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
        a = math.acos(cos_a)
    except Exception:
        return
    # TODO: check the following formula
    # alpha = - math.atan2(sqrt(1-cos_a**2), cos_a)
    theta2 = 2*pi - a
    theta1 = math.atan2(x, y) \
               - math.atan2(L2*sin(theta2), L1+L2*cos(theta2))
    # print ("cos_a: ", cos_a, "alpha: ", alpha/pi*180, "theta1: ",theta1/pi*180,"theta2",theta2/pi*180)
    #calculate motor torque M2
    alpha = math.atan2(380,300)
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
    theta5 = math.acos((L2**2+L4**2-L1**2)/(2*L2*L4))
    M1 = m2*g*cos(theta4)*L3 + F*cos(gamma)*cos(theta5)*L4 \
            - 0.5*m1*g*L1*sin(theta1) - w2*g*L1*sin(theta1)
    return (M1, M2)

X2s = linspace(-0.3,0.3,10)
L1s = linspace(0.3, 1.5, 10)
L2s = linspace(0.3, 1.5, 10)

M1s = []
M2s = []
for X2 in X2s:
    for L1 in L1s:
        for L2 in L2s:
            result = compute(X2,Y2)
            if result!=None:
                M1s.append(abs(result[0]))
                M2s.append(abs(result[1]))
        
print("max M1: ", max(M1s), ", max M2: ", max(M2s))

