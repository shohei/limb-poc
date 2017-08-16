clear all; close all;


L1 = 2;
L2 = 2;
theta1 = 60;
theta2 = 45;

x0 = [0,0];
x1 = [L1*cos(theta1*pi/180),L1*sin(theta1*pi/180)];
x2 = [x1(1)+L2*cos(theta2*pi/180),x1(2)+L2*sin(theta2*pi/180)];

node1(x0);
node2(x1);
link1(x0,x1);
link2(x1,x2);

if(theta1<90)
   if(theta2<180) 
   
   elseif(theta2>=180)
       
   end
elseif (theta1>=90)
    if (theta2<180)
        
    elseif(theta2>=180)
        
    end
end



function node1(x)
circle(x);
end

function node2(x)
circle(x);
end

function link1(x0,x1)
line(x0,x1);
end

function link2(x0,x1)
line(x0,x1);
end

function circle(x)
r = 0.1;
ang=0:0.01:2*pi;
xp=r*cos(ang);
yp=r*sin(ang);
plot(x(1)+xp,x(2)+yp,'r','LineWidth',2);
axis equal;
hold on;
end

function line(x0,x1)
xs = linspace(x0(1),x1(1),10);
ys = linspace(x0(2),x1(2),10);
plot(xs,ys,'b','LineWidth',2);
hold on;
end

