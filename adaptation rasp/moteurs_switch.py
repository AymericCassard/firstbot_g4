import time
import pypot.dynamixel

import numpy as np
import cv2 as cv2
webcam = cv2.VideoCapture(0)


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
    # masque marron
    lower_brown = np.array([10, 100, 20])
    upper_brown = np.array([20, 255, 200])
    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
    result_brown = cv2.bitwise_and(degraded, degraded, mask=mask_brown)

    jaune_trouve=[]
    rouge_trouve=[]
    bleu_trouve=[]
    marron_trouve=[]

    h, w, c = result_blue.shape

    #moyenne bleu
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_blue[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if b!=0:
                bleu_trouve.append(x)
    if(len(bleu_trouve)!=0):
        moyenne_blue = sum(bleu_trouve) // len(bleu_trouve)-w//2
        #print("Moyenne bleu: ", moyenne_blue-w//2)
    else:
        moyenne_blue=1000

    #moyenne rouge
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_red[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                rouge_trouve.append(x)
    if(len(rouge_trouve)!=0):
        moyenne_red = sum(rouge_trouve) // len(rouge_trouve)-w//2
        #print("Moyenne rouge: ", moyenne_red-w//2)
    else:
        moyenne_red=1000

    #moyenne jaune
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_yellow[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                jaune_trouve.append(x)
    if(len(jaune_trouve)!=0):
        moyenne_yellow = sum(jaune_trouve) // len(jaune_trouve)-w//2
        #print("Moyenne jaune: ", moyenne_yellow-w//2)
    else:
        moyenne_yellow=1000

    #comptage marron
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_brown[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                marron_trouve.append(x)

    if len(marron_trouve) > len(jaune_trouve) and \
       len(marron_trouve) > len(rouge_trouve) and \
       len(marron_trouve) > len(bleu_trouve):
       return True
    else:
        return [moyenne_blue, moyenne_red, moyenne_yellow]

def moyenne_couleurs_full_image(img):
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
    marron_trouve=[]

    h, w, c = result_blue.shape

    #moyenne bleu
    for y in range(h):
        for x in range(w):
            b, g, r = result_blue[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if b!=0:
                bleu_trouve.append(x)
    if(len(bleu_trouve)!=0):
        moyenne_blue = sum(bleu_trouve) // len(bleu_trouve)-w//2
        #print("Moyenne bleu: ", moyenne_blue-w//2)
    else:
        moyenne_blue=1000

    #moyenne rouge
    for y in range(h):
        for x in range(w):
            b, g, r = result_red[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                rouge_trouve.append(x)
    if(len(rouge_trouve)!=0):
        moyenne_red = sum(rouge_trouve) // len(rouge_trouve)-w//2
        #print("Moyenne rouge: ", moyenne_red-w//2)
    else:
        moyenne_red=1000

    #moyenne jaune
    for y in range(h):
        for x in range(w):
            b, g, r = result_yellow[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                jaune_trouve.append(x)
    if(len(jaune_trouve)!=0):
        moyenne_yellow = sum(jaune_trouve) // len(jaune_trouve)-w//2
        #print("Moyenne jaune: ", moyenne_yellow-w//2)
    else:
        moyenne_yellow=1000

    #comptage marron
    for y in range(h):
        for x in range(w):
            b, g, r = result_brown[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                jaune_trouve.append(x)

    if len(marron_trouve) > len(jaune_trouve) and \
       len(marron_trouve) > len(rouge_trouve) and \
       len(marron_trouve) > len(bleu_trouve):
       return True
    else:
        return [moyenne_blue, moyenne_red, moyenne_yellow]

ports = pypot.dynamixel.get_available_ports()
if not ports:
    exit('No port')

dxl_io = pypot.dynamixel.DxlIO(ports[0])
dxl_io.set_wheel_mode([1])

dxl1=1
dxl2=2

base_speed = 400  # vitesse de base
Kp = 12          # gain proportionnelcd
Kd = 1.0        # dérivée
dt = 0.1  # intervalle de temps entre deux mesures (en sec)
previous_error=0
target = 0 # couleur recherchee

ret, frame = webcam.read()
positions_couleurs= moyenne_couleurs(frame)

t1 = time.time()
marron_found = True
while(True):
    t2 = time.time()

    # on ne set pas les moteurs quand on trouve du marron
    if positions_couleurs is True and (t1 - t2) > 10:
        t1 = t2
        print("marron_found")

    if(positions_couleurs[0]!=1000):
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
        positions_couleurs= moyenne_couleurs(frame)
    else:
        if(previous_error>0):
            left_speed  = 100
            right_speed = 100
        else:
            left_speed  = -100
            right_speed = -100
        dxl_io.set_moving_speed({dxl1: left_speed})
        dxl_io.set_moving_speed({dxl2: right_speed})

        ret, frame = webcam.read()
        positions_couleurs= moyenne_couleurs_full_image(frame)

    #cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #time.sleep(0.1)
webcam.release()
#cv2.destroyAllWindows()

