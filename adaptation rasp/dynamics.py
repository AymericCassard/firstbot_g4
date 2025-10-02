import numpy as np
import time
import turtle
#import pypot.dynamixel

R_roue = 51.5 / 2 / 1000
d = 135 / 1000
last_time = time.time()

def deg2rad(deg):
    return deg * np.pi / 180

def rad2deg(rad):
    return rad * 180 / np.pi

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
        dxr = - R*(1 - np.cos(dtheta))
        dyr = R*(np.sin(dtheta))
        print("dxr :", dxr, "dyr :", dyr)
    x += dxr*np.cos(dtheta) - dyr*np.sin(dtheta)
    y += dxr*np.sin(dtheta) + dyr*np.cos(dtheta)
    return x, y

def detect_path(f, g, diff_time, x, y, theta, dxl_io, dxl1=1, dxl2=2):

    print("########## detect_path ########## ")
    dt = diff_time
    wl = deg2rad(-1 * dxl_io.get_present_speed([dxl1])[0])
    wr = deg2rad(dxl_io.get_present_speed([dxl2])[0])
    g.write(str(diff_time)+","+str(wl)+","+str(wr)+"\n")
    g.flush()
    
    if wl == wr:
        v = wl*R_roue
        return x + v*dt*np.cos(theta), y + R_roue*wr*dt*np.sin(theta), theta
    print("wl :",rad2deg(wl),"wr :", rad2deg(wr))
    R, w = direct(wl, wr)
    print("R :",R,"w :", w)
    x, y = ICR_to_coo(R, w, x, y, dt)
    theta += w*dt

    f.write(str(x)+","+str(y)+","+str(theta)+"\n")
    f.flush()

    return x,y, theta


    
