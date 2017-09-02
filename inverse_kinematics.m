close all;clear;format compact;

count=0;
for x2 = linspace(0,-0.2,4)
    y2 = 1;
    for L1=linspace(0.3,1,5)
        for L2=linspace(0.3,1,5)
            try
                theta3_rad = acos((x2^2+y2^2-L1^2-L2^2)/(2*L1*L2));
                theta3 = theta3_rad * 180 / pi;
                %theta3;
                
                theta1_rad  = atan2(y2,x2) -...
                    atan2(sqrt(4*L1^2*L2^2-(x2^2+y2^2-L1^2-L2^2)^2), ...
                    2*L1^2+(x2^2+y2^2+L1^2-L2^2));
                theta1 = theta1_rad * 180/pi;
                
                x1 = L1*cos(theta1_rad);
                y1 = L1*sin(theta1_rad);
                
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
                set(gca,'XDir','reverse')
                
                title(sprintf('x2:%.1f L1:%.2f L2:%.2f',x2,L1,L2));
                pause(0.3);
                str=sprintf('x2=%.2f, L1=%.2f, L2=%.2f, theta1=%.2f, theta2=%.2f',...
                    x2,L1,L2,180-theta1,theta3);
                str
            catch
            end
        end
    end
    
end


