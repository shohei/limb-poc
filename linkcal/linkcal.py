#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
Motor torque calculator
Shokara Inc. 2017
"""

import warnings
warnings.filterwarnings("ignore")
import math
from pylab import *
import pdb
import numpy as np
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
import csv
import configparser
import os
import sys

# preset parameter
x_offset = 0.38
Y2 = 1 # [m]
Wtotal = 60 #[kg]
rate = 0.82 # rate of weight over the knees
W = Wtotal*rate
g = 9.8 # gravity
m1 = 1 # [kg]
m2 = 1 # [kg]
w1 = 1 # [kg]
w2 = 1 # [kg]
y_final = 1.4

"""
Function definitions
"""

def linear_interpolation(x0,y0,x1,y1):
    a = (y1-y0)/(x1-x0)
    b = y0 - a*x0
    xs = linspace(x0,x1,10)
    ys = [a*x+b for x in xs] 
    return (xs,ys) 

def is_valid_x2(x, y):
    if(sqrt(x**2+y**2) - (L1 + L2)<0):
        return True
    else:
        print("triangle inequality not satisfied")
        return False

def forward_kinematics(L1, L2, theta1,theta2):
    theta3 = theta1+theta2 - pi
    x0 = [0,0]
    x1 = [L1*cos(theta1),L1*sin(theta1)]
    x2 = [x1[0]+L2*cos(theta3),x1[1]+L2*sin(theta3)]

def forward_kinematics_draw(L1, L2, theta1,theta2):
    theta3 = theta1+theta2 - pi
    x0 = [0,0]
    x1 = [L1*cos(theta1),L1*sin(theta1)]
    x2 = [x1[0]+L2*cos(theta3),x1[1]+L2*sin(theta3)]
    show_stick(x0,x1,x2)

def show_stick(x0,x1,x2):
    circle(x0)
    circle(x1)
    line(x0,x1)
    line(x1,x2)

def circle(xc):
    r = 0.02
    ang=linspace(0,2*pi,20)
    xp=[r*cos(a) for a in ang]
    yp=[r*sin(a) for a in ang]
    xcp = [xc[0] + x for x in xp]
    ycp = [xc[1] + y for y in yp]
    plot(xcp,ycp,"r",linewidth=2)
    axis('equal')

def line(x0,x1):
    xs = linspace(x0[0],x1[0],10)
    ys = linspace(x0[1],x1[1],10)
    plot(xs,ys,"b",linewidth=2)

def inverse_kinematics(x, y):
    cos_a = (-(x**2+y**2)+L1**2+L2**2)/(2*L1*L2)
    try:
        a = - math.atan2(sqrt(1 - cos_a**2), cos_a)
    except Exception:
        # print("a fail and exit")
        return
    theta2 = 2*pi - a
    theta2_dash = pi - a
    theta1 = math.atan2(y, x) \
               - math.atan2(L2*sin(theta2_dash), L1+L2*cos(theta2_dash))
    #calculate motor torque M2
    alpha = math.atan2(380,600)
    F = W*g*sin(alpha)
    theta3 = theta1+theta2-pi
    gamma = alpha + theta3 - pi/2
    M2 = 0.5*L2*m2*g*cos(theta3) + F*L2*cos(gamma)
    #calculate motor torque M1
    L3 = sqrt(L1**2 + (L2/2)**2 - 2*L1*(L2/2)*cos(theta2)) # The therom of cosines
    L4 = sqrt(L1**2 + L2**2 - 2*L1*L2*cos(theta2))
    try:
        alpha1 = math.acos((L3**2-(L2/2)**2-L1**2)/(2*L3*(L2/2)))
    except Exception:
        # print("alpha1 fail and exit")
        return
    alpha2 = pi/2 - (theta3+alpha1)
    theta4 = pi/2 - alpha2
    try:
        theta5 = math.acos((L2**2+L4**2-L1**2)/(2*L2*L4))
    except Exception:
        # print("theta5 fail and exit")
        return

    M1 = m2*g*cos(theta4)*L3 + F*cos(gamma)*cos(theta5)*L4 \
            - 0.5*m1*g*L1*sin(theta1) - w2*g*L1*sin(theta1)
    M1_static = m2*g*cos(theta4)*L3 - 0.5*m1*g*L1*sin(theta1) - w2*g*L1*sin(theta1)

    M1 = max(abs(M1),abs(M1_static))
    if(math.isnan(M1) or math.isnan(M2)):
        # print("M1 or M2 is NaN")
        return

    forward_kinematics(L1, L2, theta1,theta2)
    if(theta2>2*pi):
        theta2 = theta2 - 2*pi
    return (abs(M1), abs(M2), theta1, theta2)

def usage():
    sys.stderr.write("Usage: " + sys.argv[0] + " .ini file\n")
    return

def show_config(ini):
    for section in ini.sections():
        print ("[" + section + "]")
        show_section(ini, section)
    return

def show_section(ini, section):
    for key in ini.options(section):
        show_key(ini, section, key)
    return

def show_key(ini, section, key):
    print (section + "." + key + " = " + ini.get(section, key))
    return


def set_value(ini, section, key, value):
    ini.set(section, key, value)
    print (section + "." + key + " = " + ini.get(section, key))
    return

def print_title():
    title =     '''
/*************************************************/
/*  _       _           _                     _  */
/* | |     (_)  _ __   | | __   ___    __ _  | | */
/* | |     | | | '_ \  | |/ /  / __|  / _` | | | */
/* | |___  | | | | | | |   <  | (__  | (_| | | | */
/* |_____| |_| |_| |_| |_|\_\  \___|  \__,_| |_| */
/*                                               */
/*************************************************/
'''
    print(title)

"""
Main program area
"""
argc = len(sys.argv)
if argc == 1:
    usage()
    sys.exit(1)

INI_FILE = sys.argv[1]
ini = configparser.SafeConfigParser()
if os.path.exists(INI_FILE):
    ini.read(INI_FILE, encoding='utf8')
else:
    sys.stderr.write(INI_FILE + "not found")
    sys.exit(2)

print_title()

if argc == 2:
    show_config(ini)
    print()

L1min = float(ini.get("Parameters", "l1min"))
L1max = float(ini.get("Parameters", "l1max"))
L2min = float(ini.get("Parameters", "l2min"))
L2max = float(ini.get("Parameters", "l2max"))
X2min = float(ini.get("Parameters", "x2min"))
X2max = float(ini.get("Parameters", "x2max"))
Y2 = float(ini.get("Parameters", "y2"))
Wtotal = float(ini.get("Parameters", "wtotal"))
rate = float(ini.get("Parameters", "rate"))
m1 = float(ini.get("Parameters", "m1"))
m2 = float(ini.get("Parameters", "m2"))
w1 = float(ini.get("Parameters", "w1"))
w2 = float(ini.get("Parameters", "w2"))
y_final = float(ini.get("Parameters", "y_final"))

X2s = linspace(X2min, X2max,10)
L1s = linspace(L1min, L1max, 10)
L2s = linspace(L2min, L2max, 10)

maxM1s = []
maxParams = []
maxCount = len(X2s)*len(L1s)*len(L2s)
counter = 0
for X2 in X2s:
    for L1 in L1s:
        for L2 in L2s:
            M1s = []
            M2s = []
            params = []
            x_final = X2-0.38
            (xs, ys) = linear_interpolation(X2, Y2, x_final, y_final)
            for idx, x in enumerate(xs):
                y = ys[idx]
                result = inverse_kinematics(x,y)
                if result!=None:
                    M1s.append(abs(result[0]))
                    M2s.append(abs(result[1]))
                    params.append((X2,L1,L2,result[2],result[3]))
            if M1s==[]:
                continue 
            i1 = M1s.index(max(M1s))
            # i2 = M2s.index(max(M2s))
            maxM1s.append(max(M1s))
            maxParams.append(params[i1])
            percentage = int(counter*1.0/maxCount*100)
            print("calculating",percentage,"%",end='\r')
            counter = counter + 1

myarray = np.array(maxM1s)
K = 10 
unsorted_max_indices = np.argpartition(myarray, K)[:K]
y = myarray[unsorted_max_indices]
indices = np.argsort(-y)
max_k_indices = unsorted_max_indices[indices]
data = []
counter = 1
for i in max_k_indices:
    data.append([round(maxM1s[i],3), round(maxParams[i][0],3), round(maxParams[i][1],3), round(maxParams[i][2],3), round(maxParams[i][3]/pi*180,3), round(maxParams[i][4]/pi*180,3)])

fig = figure(figsize=(12,10)) 
fig.patch.set_facecolor('white') 
fig.canvas.set_window_title('result')
data.reverse()
print('[Result]')
print("{:>10} {:>10} {:>10} {:>10} {:>10} {:>10}".format("Max M1","X2","L1","L2","theta1","theta2"))
for row in data:
    print("{: >10} {: >10} {: >10} {: >10} {: >10} {: >10}".format(*row))
    ax = fig.add_subplot(5,2,counter)
    ax.patch.set_facecolor('white')
    ax.set_title("Max M1:{},X2:{},L1:{},L2:{}".format(row[0],row[1],row[2],row[3]))
    axis('off')
    counter = counter + 1 
    forward_kinematics_draw(row[2],row[3],row[4]*pi/180,row[5]*pi/180)

show()
