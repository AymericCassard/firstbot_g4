import numpy as np
import time
import turtle

R_roue = 51.5 / 1000
d = 135 / 1000
x = 0
y = 0
theta = 0
last_time = time.time()
pos_list = []

def initialize(x0, y0, theta0):
    global x, y, theta, list_pos, last_time
    last_time = time.time()
    x = x0
    y = y0
    list_pos = []
    theta = theta0

def get_wheel_ang_pos():
    return 0,0

def direct(wl, wr):
    vr = R_roue*wr
    vl = R_roue*wl
    w = (vr - vl) / d 
    R = d/2 * (vr + vl)/(vr-vl)
    return R, w

def ICR_to_coo(R, w, x, y, dt):
    if w == 0:
        dx = 0
        dy = 0
        dtheta = 0
    elif R == 0:
        dx = 0
        dy = 0
        dtheta = w*dt
    else:
        dtheta = w*dt
        dx = R*(np.sin(dtheta + np.pi/2) - np.sin(np.pi/2))
        dy = -R*(np.cos(dtheta + np.pi/2) - np.cos(np.pi/2))
    x += dx
    y += dy
    return x, y

def detect_path():
    global x, y, theta, last_time
    dt = time.time() - last_time
    last_time = time.time()
    thetal, thetar = get_wheel_ang_pos()
    wl = thetal / dt
    wr = thetar / dt
    R, w = direct(wl, wr)
    x, y = ICR_to_coo(R, w, 0, 0, dt)
    theta += w*dt
    pos_list.append((x, y, theta))

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
    t.penup()
    for pos in pos_list:
        x, y, theta = pos
        t.goto(x*1000, y*1000)
        t.pendown()
    t.penup()
    turtle.done()





    
