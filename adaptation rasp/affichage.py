import time
import turtle

f = open("positions.txt", "r")

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



list_pos_to_draw()