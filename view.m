function varargout = view(varargin)
% VIEW MATLAB code for view.fig
%      VIEW, by itself, creates a new VIEW or raises the existing
%      singleton*.
%
%      H = VIEW returns the handle to a new VIEW or the handle to
%      the existing singleton*.
%
%      VIEW('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in VIEW.M with the given input arguments.
%
%      VIEW('Property','Value',...) creates a new VIEW or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before view_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to view_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help view

% Last Modified by GUIDE v2.5 16-Aug-2017 08:19:39

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @view_OpeningFcn, ...
                   'gui_OutputFcn',  @view_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before view is made visible.
function view_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to view (see VARARGIN)

% Choose default command line output for view
handles.output = hObject;
handles.theta1 = 0;
handles.theta2 = 0;
handles.L1 = 0.5;
handles.L2 = 0.5;
% Update handles structure
guidata(hObject, handles);
% UIWAIT makes view wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = view_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;
varargout{2} = 0;

% --- Executes on slider movement.
function slider1_Callback(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
handles.theta1 = get(hObject,'Value');
guidata(hObject,handles);
theta1 = handles.theta1;
theta2 = handles.theta2;
L1 = handles.L1;
L2 = handles.L2;
theta1_theta2 = sprintf('%.2f, %.2f',theta1,theta2);
% theta1_theta2
axes(handles.axes1);
drawAxis(L1,L2,theta1,theta2);
axes(handles.axes3);
cla;
initM2;
% set(handles.axes3,'view',[-37.5 30]);
rotate3d;
hold on;
m1 = 0.2;
m2 = 0.2;
g = 9.8;
L1 = 0.5;
L2 = 0.5;
w1 = 0.3;
w2 = 0.3;
F = 60;
M2 = F*L2*cos((theta1+theta2-180)*pi/180) + m2*g*cos((theta1+theta2-180)*pi/180);
plot3(theta1,theta2,M2,'ro','LineWidth',10);

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider


% --- Executes during object creation, after setting all properties.
function slider1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


% --- Executes on slider movement.
function slider2_Callback(hObject, eventdata, handles)

handles.theta2 = get(hObject,'Value');
guidata(hObject,handles);
theta1 = handles.theta1;
theta2 = handles.theta2;
L1 = handles.L1;
L2 = handles.L2;
theta1_theta2 = sprintf('%.2f, %.2f',theta1,theta2);
% theta1_theta2
axes(handles.axes1);
drawAxis(L1,L2,theta1,theta2);
axes(handles.axes3);
cla;
initM2;
% set(handles.axes3,'view',[-37.5 30]);
rotate3d;
hold on;
m1 = 0.2;
m2 = 0.2;
g = 9.8;
L1 = 0.5;
L2 = 0.5;
w1 = 0.3;
w2 = 0.3;
F = 60;
M2 = F*L2*cos((theta1+theta2-180)*pi/180) + m2*g*cos((theta1+theta2-180)*pi/180);
plot3(theta1,theta2,M2,'ro','LineWidth',10);

% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'Value') returns position of slider
%        get(hObject,'Min') and get(hObject,'Max') to determine range of slider

% --- Executes during object creation, after setting all properties.
function slider2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to slider2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: slider controls usually have a light gray background.
if isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor',[.9 .9 .9]);
end


function drawAxis(L1,L2,theta1,theta2)
x0 = [0,0];
x1 = [L1*cos(theta1*pi/180),L1*sin(theta1*pi/180)];
x2 = [x1(1)+L2*cos((theta2+theta1-180)*pi/180),x1(2)+L2*sin((theta2+theta1-180)*pi/180)];

cla;
xlim([-1,1]);
ylim([-1,1]);
node1(x0);
node2(x1);
link1(x0,x1);
link2(x1,x2);

function initM2
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


function circle(x)
r = 0.01;
ang=0:0.01:2*pi;
xp=r*cos(ang);
yp=r*sin(ang);
plot(x(1)+xp,x(2)+yp,'r','LineWidth',2);
axis equal;
hold on;

function line(x0,x1)
xs = linspace(x0(1),x1(1),10);
ys = linspace(x0(2),x1(2),10);
plot(xs,ys,'b','LineWidth',2);
hold on;

function node1(x)
circle(x);

function node2(x)
circle(x);

function link1(x0,x1)
line(x0,x1);

function link2(x0,x1)
line(x0,x1);
