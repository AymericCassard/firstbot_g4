import time
import matplotlib.pyplot as plt

f = open("positions.txt", "r")
x_list, y_list = [], []

def list_pos_to_draw():
    for line in f.readlines():
        x_str, y_str, theta_str = line.strip().split(",")
        x, y, theta = float(x_str), float(y_str), float(theta_str)
        x_list.append(x*1000)
        y_list.append(y*1000)
    plt.plot(x_list, y_list, marker='o')
    plt.title("Trajectoire du robot")
    plt.show()


list_pos_to_draw()