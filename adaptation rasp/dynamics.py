import numpy as np
import time
import turtle
#import pypot.dynamixel

R_roue = 51.5 / 2 / 1000
d = 135 / 1000
last_time = time.time()

"""data_f = open("data.txt", "r")
x_list, y_list = [], []

data = []
data_index = 0
for line in data_f.readlines():
    time_diff, v1, v2 = line.strip().split(",")
    time_diff, v1,v2 = float(time_diff), float(v1), float(v2)
    data.append([time_diff, v1, v2])

def next_data():
    global data_index
    data_value = data[data_index]
    data_index += 1
    if data_index >= len(data) :
        print("bonjour")
        exit()
    return data_value
""" 

def deg2rad(deg):
    return deg * np.pi / 180

def rad2deg(rad):
    return rad * 180 / np.pi

def direct(wl, wr):
    vr = R_roue*wr
    vl = R_roue*wl
    w = (vr - vl) / d 
    R = d/2 * (vr + vl)/(vr-vl)
    print("d :",d, "vr :",vr, "vl :",vl)
    return R, w

def ICR_to_coo(R, w, x, y, dt, theta):
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
    x += dxr*np.cos(theta) - dyr*np.sin(theta)
    y += dxr*np.sin(theta) + dyr*np.cos(theta)
    return x, y

def detect_path(f, g, diff_time, x, y, theta, dxl_io, dxl1=1, dxl2=2):
    
    print("########## detect_path ########## ")
    dt = diff_time
    wr = deg2rad(-1 * dxl_io.get_present_speed([dxl1])[0])
    wl = deg2rad(dxl_io.get_present_speed([dxl2])[0])
    #g.write(str(diff_time)+","+str(wl)+","+str(wr)+"\n")
    #g.flush()

    #data_values = next_data()
    #dt, wr, wl = data_values[0], data_values[1], data_values[2]
    
    if wl == wr:
        v = wl*R_roue
        return x + v*dt*np.cos(theta), y + R_roue*wr*dt*np.sin(theta), theta
    print("wl :",rad2deg(wl),"wr :", rad2deg(wr))
    R, w = direct(wl, wr)
    print("R :",R,"w :", w)
    x, y = ICR_to_coo(R, w, x, y, dt, theta)
    theta += w*dt
    print("theta :", rad2deg(theta))

    f.write(str(x)+","+str(y)+","+str(theta)+"\n")
    f.flush()

    return x,y, theta


    
