close all;
clear;
format compact;

cols = [];

for x2 = linspace(0.3,0,3)
    y2 = 1;
    for L1=linspace(0.3,1,5)
        for L2=linspace(0.3,1,5)
            try
                cosa = (-(x2^2+y2^2)+L1^2+L2^2)/(2*L1*L2);
                alpha = -atan2(sqrt(1-(cosa)^2),cosa);
                theta2 = pi - alpha;
                theta1 = atan2(y2,x2) - atan2(L2*sin(theta2),L1+L2*cos(theta2));
                
                x1 = L1*cos(theta1);
                y1 = L1*sin(theta1);
                
                L1a = sqrt(x1^2+x2^2);
                L2a = sqrt((x2-x1)^2+(y2-y1)^2);
                err1 = abs(L1-L1a);
                err2 = abs(L2-L2a);
                
                px1  = [0,x1];
                py1 = [0,y1];
                px2 = [x1,x2];
                py2 = [y1,y2];
                
                cla;
                plot(px1,py1,'LineWidth',2);
                hold on;
                plot(px2,py2,'LineWidth',2);
                xlim([-1.2,1.2]);
                ylim([-0.2,1.2]);
                
                title(sprintf('x2:%.1f L1:%.2f L2:%.2f',x2,L1,L2));
%                 pause(0.3);
                %                 str=sprintf('x2=%.2f, L1=%.2f, L2=%.2f, theta1=%.2f, theta2=%.2f',...
                %                     x2,L1,L2,theta1*180/pi,2*pi-alpha*180/pi);
                col = [x2,L1,L2,theta1*180/pi,2*pi-alpha*180/pi];
                cols = vertcat(cols,col);
            catch
            end
        end
    end    
end
cols

csvwrite('hoge.csv',cols);

