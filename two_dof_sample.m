%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Robot 2dof
% Toa do khau cuoi
% x = a2*cos(theta2) + a1
% y = 0
% z = a2*sin(theta2) + d1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Ve do thi bai toan dong hoc thuan 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Quy luat chuyen dong
%   theta2 = sin(2*pi*t)
%   d1 = 7*(sin(2*t))^2
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Thong so cua robot
clear all
clc;
a1 = 600; % mm
a2 = 500; % mm
t = 0:0.05:10; % Thoi gian la 10s
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
theta2 = sin(2*pi*t);
d1 = 7*(sin(2*t)).^2;
x = a2*cos(theta2) + a1;
y = zeros(1,length(t));
z = a2*sin(theta2) + d1;

% Ve do thi toa do khau cuoi
figure(1)
title('Quy dao cua khau tac dong cuoi trong bai toan thuan')
hold on
grid on
view(3);
for k = 1:length(t)
    plot3(x(1,k),y(1,k),z(1,k),'bx');
    pause(0.01);
end

% Ve do thi van toc khau cuoi
V_x = diff(x); % Van toc theo phuong x
V_y = diff(y); % Van toc theo phuong y
V_z = diff(z); % van toc theo phuong z
figure(2)
title('Van toc khau tac dong cuoi')
grid on
hold on
plot(diff(t),V_x,'b','LineWidth',2);
plot(diff(t),V_y,'r','LineWidth',2);
plot(diff(t),V_z,'g','LineWidth',2);
legend('V_x','V_y','V_z');
% Dong hoc nguoc
% Vi du ve duong thang di qua 2 diem A(800,0,200) va B(600,0,400)
% Moi diem la 1 hang, co the mo rong di qua nhieu diem
xyz_spaces = [800 0 200;...
             600 0 400];
joint_spaces = zeros(2,2);
[row,col] = size(xyz_spaces);
for k = 1: row
    x = xyz_spaces(k,1); % To do x
    y = xyz_spaces(k,2); % Toa do y
    z = xyz_spaces(k,3); % Toa do z
    if x > 1100 || x < 100 || y ~= 0 || z > 1000 || z < 0
        display('Toa do bi sai kia!');
        break;
    end
    d1_1 = z - sqrt(a2^2 - (x - a1)^2);
    d1_2 = z + sqrt(a2^2 - (x - a1)^2);
    if d1_1 <= 1000 && d1_1 >= 0
        joint_spaces(k,1) = d1_1;
    else
        joint_spaces(k,1) = d1_2;
    end
    d1 = joint_spaces(k,1);
    joint_spaces(k,2) = atan2d((z - d1)/a2,(x - a1)/a2);
end

% Ve do thi dong hoc nguoc
figure (3)
subplot(2,1,1);
grid on
hold on
title('Toa do XYZ')
plot([0,10],xyz_spaces(:,1),'b','LineWidth',2); % X
plot([0,10],xyz_spaces(:,2),'r','LineWidth',2); % Y
plot([0,10],xyz_spaces(:,3),'g','LineWidth',2); % Z
legend('X','Y','Z');
subplot(2,1,2);
grid on
hold on
title('Bien khop')
plot([0,10],joint_spaces(:,1),'b','LineWidth',2); % d1
plot([0,10],joint_spaces(:,2),'r','LineWidth',2); % theta2
legend('d1','theta2');