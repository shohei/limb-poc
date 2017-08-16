clear all; close all;

m1 = 0.2;
m2 = 0.2;
g = 9.8;
L1 = 0.5;
L2 = 0.5;
w1 = 0.3;
w2 = 0.3;
F = 60;

theta1 = linspace(0,180,31);
theta2 = linspace(0,360,31);
[X,Y] = meshgrid(theta1,theta2);
M2 = F*L2*cos((X+Y-180)*pi/180) + m2*g*cos((X+Y-180)*pi/180);
surf(X,Y,M2);
hold on;

theta1 = 30;
theta2 = 30;
M2 = F*L2*cos((theta1+theta2-180)*pi/180) + m2*g*cos((theta1+theta2-180)*pi/180);
plot3(theta1,theta2,M2,'ro','LineWidth',10);



