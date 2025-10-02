import time
import dynamics
import pypot.dynamixel

import numpy as np
import cv2 as cv2
webcam = cv2.VideoCapture(0)

#VARIABLE
camera_time = time.time()
last_time = time.time()
f = open("positions.txt", "w+")
camera_index = 0
x, y, theta = 0, 0, 0

#BOOLEANS
detect_line = True
capture_positions = True


def moyenne_couleurs(img):
    small = cv2.resize(img, (0,0), fx=0.10, fy=0.10, interpolation=cv2.INTER_AREA)
    cv2.imwrite("compressed.jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 20])
    degraded = cv2.imread("compressed.jpg")
    #cv2.imshow("Image compressée", degraded)

    hsv = cv2.cvtColor(degraded, cv2.COLOR_BGR2HSV)

    #masque bleu
    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    result_blue = cv2.bitwise_and(degraded, degraded, mask=mask_blue)
    #masque rouge
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    result_red = cv2.bitwise_and(degraded, degraded, mask=mask_red)
    #masque jaune
    lower_yellow = np.array([20, 100, 50])
    upper_yellow = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    result_yellow = cv2.bitwise_and(degraded, degraded, mask=mask_yellow)

    jaune_trouve=[]
    rouge_trouve=[]
    bleu_trouve=[]

    h, w, c = result_blue.shape

    #moyenne bleu
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_blue[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if b!=0:
                bleu_trouve.append(x)
    if(len(bleu_trouve)!=0):
        moyenne_blue = sum(bleu_trouve) // len(bleu_trouve)
        #print("Moyenne bleu: ", moyenne_blue-w//2)
    else:
        moyenne_blue=0

    #moyenne rouge
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_red[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                rouge_trouve.append(x)
    if(len(rouge_trouve)!=0):
        moyenne_red = sum(rouge_trouve) // len(rouge_trouve)
        #print("Moyenne rouge: ", moyenne_red-w//2)
    else:
        moyenne_red=0

    #moyenne jaune
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_yellow[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                jaune_trouve.append(x)
    if(len(jaune_trouve)!=0):
        moyenne_yellow = sum(jaune_trouve) // len(jaune_trouve)
        #print("Moyenne jaune: ", moyenne_yellow-w//2)
    else:
        moyenne_yellow=0

    return [moyenne_blue-w//2, moyenne_red-w//2, moyenne_yellow-w//2]


if detect_line :
    ports = pypot.dynamixel.get_available_ports()
    if not ports:
        exit('No port')

    dxl_io = pypot.dynamixel.DxlIO(ports[0])
    dxl_io.set_wheel_mode([1])

    dxl1=1
    dxl2=2

#g = open("data.txt", "w+")

while(True):
    if detect_line :
        ret, frame = webcam.read()

        positions_couleurs= moyenne_couleurs(frame)
        #print(positions_couleurs)
        base_speed = 100  # vitesse de base
        Kp = 2.0          # gain proportionnel (à ajuster)

        # Exemple avec la valeur venant du suivi de couleur
        error_blue = positions_couleurs[0] 

        # Calcul des vitesses avec correction proportionnelle
        left_speed  = - (base_speed - Kp * error_blue)
        right_speed =   (base_speed + Kp * error_blue)

        # Envoi aux moteurs
        dxl_io.set_moving_speed({dxl1: left_speed})
        dxl_io.set_moving_speed({dxl2: right_speed})

        #cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if capture_positions :
        diff_time = time.time() - last_time
        if diff_time > 0.02:  # Capture every 0.1 seconds
            last_time = time.time()
            x, y, theta = dynamics.detect_path(f, "g", diff_time, x, y, theta, dxl_io, dxl1, dxl2)
    
    if camera_time + 5 < time.time():
        camera_time = time.time() 
        camera_index += 1
        cv2.imwrite("images/image"+str(camera_index)+".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        print("Image saved")  

webcam.release()
#cv2.destroyAllWindows()

 
for i in range(1):
	dxl_io.set_moving_speed({dxl1: -500})
	dxl_io.set_moving_speed({dxl2: 500})
	time.sleep(5)
	dxl_io.set_moving_speed({dxl1: 0})
	dxl_io.set_moving_speed({dxl2: 0})
	time.sleep(1)

f.close()
#g.close()