import numpy as np
import time
import turtle
import threading
#import pypot.dynamixel

R_roue = 51.5 / 1000
d = 135 / 1000
x = 0
y = 0
theta = 0
last_time = time.time()
f = open("positions.txt", "w+")

def deg2rad(deg):
    return deg * np.pi / 180

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
    global x, y, theta, last_time
    dt = time.time() - last_time
    last_time = time.time()
    #thetal, thetar = get_wheel_ang_pos(dxl_io, dxl1, dxl2)
    #wl = thetal / dt
    #wr = thetar / dt
    R, w = direct(deg2rad(wl), deg2rad(wr))
    x, y = ICR_to_coo(R, w, x, y, dt)
    theta += w*dt
    
    f.write(str(x)+","+str(y)+","+str(theta)+"\n")

def list_pos_to_draw():
    fenetre = turtle.Screen()
    fenetre.title("Tortue Python 🐢")
    fenetre.bgcolor("lightblue")

    # Créer la tortue
    t = turtle.Turtle()
    t.shape("turtle")
    t.color("green")
    t.speed(3)
    t.clear()
    t.pendown()
    for line in f.readlines():
        x_str, y_str, theta_str = line.strip().split(",")
        x, y, theta = float(x_str), float(y_str), float(theta_str)
        t.goto(x*1000, y*1000)
    t.penup()
    turtle.done()




    
