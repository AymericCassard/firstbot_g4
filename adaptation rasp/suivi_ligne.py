import time
import pypot.dynamixel
import dynamics
import numpy as np
import cv2 as cv2
import couleur

webcam = cv2.VideoCapture(0)



#VARIABLE
camera_time = time.time()
last_time = time.time()
f = open("positions.txt", "w+")
camera_index = 0
x, y, theta = 0, 0, 0

#BOOLEANS
follow_line = False
capture_positions = True
capture_images = True

#Initalisation moteurs

ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_wheel_mode([1])

dxl1=1
dxl2=2

base_speed = 250  # vitesse de base
Kp = 8     # gain proportionnelcd
Kd = 0.0      # dérivée
dt = 0.1  # intervalle de temps entre deux mesures (en sec)
previous_error=0

ret, frame = webcam.read()
positions_couleurs= couleur.moyenne_couleurs(frame)

stuck = False

if not follow_line :
    dxl_io.disable_torque([1, 2])

while(True):
    if follow_line :
        if(positions_couleurs[0]<=1000):
            error = positions_couleurs[0]

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

    if capture_positions :
        diff_time = time.time() - last_time
        if diff_time > 0.02:  # Capture every 0.1 seconds
            last_time = time.time()
            x, y, theta = dynamics.detect_path(f, "g", diff_time, x, y, theta, dxl_io, dxl1, dxl2)
    
    if capture_images and camera_time + 0.1 < time.time():
        camera_time = time.time() 
        camera_index += 1
        cv2.imwrite("images/image"+str(camera_index)+".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        print("Image saved in",time.time()-camera_time,"secondes")  


webcam.release()
#cv2.destroyAllWindows()
f.close()
