#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Motor torque calculator
Copyright Shokara Inc. 2017
"""

import math
import numpy as np
from pylab import *

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
y_final = 1400

def linear_interpolation(x0,y0,x1,y1):
    a = (y1-y0)/(x1-x0)
    b = y0 - a*x0
    xs = linspace(x0,x1,10)
    ys = [a*x+b for x in xs] 
    return (xs,ys) 

def compute(x, y):
    """arguments: x:X2, y:Y2"""
    #inverse kinematics
    cos_a = (-(x**2+y**2)+L1**2+L2**2)/(2*L1*L2)
    try:
        a = -math.atan2(sqrt(1 - cos_a**2, cos_a))
    except Exception:
        return
    theta2 = pi - a
    theta1 = math.atan2(x, y) \
               - math.atan2(L2*sin(theta2), L1+L2*cos(theta2))
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
    theta5 = math.acos((L2**2+L4**2-L1**2)/(2*L2*L4))
    M1 = m2*g*cos(theta4)*L3 + F*cos(gamma)*cos(theta5)*L4 \
            - 0.5*m1*g*L1*sin(theta1) - w2*g*L1*sin(theta1)
    return (M1, M2)

X2s = linspace(-0.3,0.3,7)
L1s = linspace(0.3, 1.5, 10)
L2s = linspace(0.3, 1.5, 10)

maxM1s = []
maxParams = []
for X2 in X2s:
    for L1 in L1s:
        for L2 in L2s:
            M1s = []
            M2s = []
            params = []
            x_final = X2-380
            (xs, ys) = linear_interpolation(X2, Y2, x_final, y_final)
            for idx, x in enumerate(xs):
                y = ys[idx]
                result = compute(x,y)
                if result!=None:
                    M1s.append(abs(result[0]))
                    M2s.append(abs(result[1]))
                    params.append((X2,L1,L2))
            if M1s==[]:
                continue 
            i1 = M1s.index(max(M1s))
            # i2 = M2s.index(max(M2s))
            maxM1s.append(max(M1s))
            maxParams.append(params[i1])

myarray = np.array(maxM1s)
K = 60 
unsorted_max_indices = np.argpartition(myarray, K)[:K]
y = myarray[unsorted_max_indices]
indices = np.argsort(-y)
max_k_indices = unsorted_max_indices[indices]
data = []
for i in max_k_indices:
    data.append([maxM1s[i], maxParams[i][0], maxParams[i][1], maxParams[i][2]])
for row in data:
    print("{: >20} {: >20} {: >20} {: >20}".format(*row))


# M1minIndex = maxM1s.index(min(maxM1s))
# M1min = maxM1s[M1minIndex]
# minParam = maxParams[M1minIndex]
#
# print("M1 min : ", M1min, ", X2: ,", minParam[0], ", L1: ", minParam[1], ", L2: ", minParam[2])

