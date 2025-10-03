import time
import pypot.dynamixel

import couleur
import numpy as np
import cv2 as cv2
webcam = cv2.VideoCapture(0)


ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_wheel_mode([1])

dxl1=1
dxl2=2


base_speed = 200  # vitesse de base
Kp = 12     # gain proportionnelcd
Kd = 0.0      # dérivée
dt = 0.1  # intervalle de temps entre deux mesures (en sec)
previous_error=0
# 0 = blue, 1 = red , 2 = yellow
target = 0

ret, frame = webcam.read()
positions_couleurs= couleur.moyenne_couleurs(frame)

tmarron = time.time() + 0

stuck = False

while(True):
    if positions_couleurs[3] > 40 and tmarron < time.time():
        print(positions_couleurs)
        print("marron trouve")
        dxl_io.set_moving_speed({dxl1: 0})
        dxl_io.set_moving_speed({dxl2: 0})
        cv2.imwrite("marron.jpg", frame)
        break
        target += 1
        tmarron = time.time() + 15
        if target > 0:
            break

    if(positions_couleurs[target]<=1000):
        error = positions_couleurs[target]

        # Proportionnelle
        P = Kp * error

        # Dérivée
        D = Kd * (error - previous_error) / dt

        # Correction totale
        correction = P + D

        # Vitesses des roues
        left_speed  = - (base_speed - correction)
        right_speed =   (base_speed + correction)

        # Envoi aux moteurs
        dxl_io.set_moving_speed({dxl1: left_speed})
        dxl_io.set_moving_speed({dxl2: right_speed})

        previous_error = error

        ret, frame = webcam.read()
        positions_couleurs= couleur.moyenne_couleurs(frame)
        stuck=False
    else:
        if(stuck==True):
            if(previous_error>0):
                left_speed  = 100
                right_speed = 100
            else:
                left_speed  = -100
                right_speed = -100
            dxl_io.set_moving_speed({dxl1: left_speed})
            dxl_io.set_moving_speed({dxl2: right_speed})

        ret, frame = webcam.read()
        positions_couleurs= couleur.moyenne_couleurs_full_image(frame)
        stuck=True

    #cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #time.sleep(0.1)
webcam.release()
#cv2.destroyAllWindows()
