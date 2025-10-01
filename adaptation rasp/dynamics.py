import numpy as np
import time
import turtle
#import pypot.dynamixel

f = open("positions.txt", "w+")

R_roue = 51.5 / 1000
d = 135 / 1000
x = 0
y = 0
theta = 0
last_time = time.time()

def deg2rad(deg):
    return deg * np.pi / 180

def rad2deg(rad):
    return rad * 180 / np.pi

def initialize(x0, y0, theta0):
    global x, y, theta, list_pos, last_time
    last_time = time.time()
    x = x0
    y = y0
    theta = theta0

def get_wheel_ang_pos(dxl_io, dxl1, dxl2):
    thetal = deg2rad(dxl_io.get_present_position([dxl1])[0])
    thetar = deg2rad(dxl_io.get_present_position([dxl2])[0])
    return thetal, thetar

def direct(wl, wr):
    vr = R_roue*wr
    vl = R_roue*wl
    w = (vr - vl) / d 
    R = d/2 * (vr + vl)/(vr-vl)
    return R, w

def ICR_to_coo(R, w, x, y, dt):
    if w == 0:
        dxr = 0
        dyr = 0
        dtheta = 0
    elif R == 0:
        dxr = 0
        dyr = 0
        dtheta = w*dt
    else:
        dtheta = w*dt
        dxr = R*(np.sin(dtheta + np.pi/2) - np.sin(np.pi/2))
        dyr = -R*(np.cos(dtheta + np.pi/2) - np.cos(np.pi/2))
    x += dxr*np.cos(dtheta) - dyr*np.sin(dtheta)
    y += dxr*np.sin(dtheta) + dyr*np.cos(dtheta)
    return x, y

def detect_path(wl, wr, dxl_io, dxl1=1, dxl2=2):
    print("detect_path")
    global x, y, theta, last_time
    dt = time.time() - last_time
    last_time = time.time()
    thetal, thetar = get_wheel_ang_pos(dxl_io, dxl1, dxl2)
    wl = deg2rad(dxl_io.get_present_speed([dxl1])[0])
    wr = deg2rad(dxl_io.get_present_speed([dxl2])[0])
    print("wl :",rad2deg(wl),"wr :", rad2deg(wr))
    R, w = direct(wl, wr)
    print("R :",R,"w :", w)
    x, y = ICR_to_coo(R, w, x, y, dt)
    theta += w*dt
    
    f.write(str(x)+","+str(y)+","+str(theta)+"\n")



    
