import time
import pypot.dynamixel
import dynamics
import numpy as np
import cv2 as cv2
import couleur

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
    marron_trouve=0

    h, w, c = result_blue.shape

    #moyenne bleu
    for y in range(5):
        for x in range(w):
            b, g, r = result_blue[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if b!=0:
                bleu_trouve.append(x)
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_blue[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if b!=0:
                bleu_trouve.append(x)
    for y in range(h-5,h):
        for x in range(w):
            b, g, r = result_blue[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if b!=0:
                bleu_trouve.append(x)
    if(len(bleu_trouve)!=0):
        moyenne_blue = sum(bleu_trouve) // len(bleu_trouve)
        #print("Moyenne bleu: ", moyenne_blue-w//2)
    else:
        moyenne_blue=10000

    #moyenne rouge
    for y in range(5):
        for x in range(w):
            b, g, r = result_red[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                rouge_trouve.append(x)
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_red[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                rouge_trouve.append(x)
    for y in range(h-5,h):
        for x in range(w):
            b, g, r = result_red[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                rouge_trouve.append(x)
    if(len(rouge_trouve)!=0):
        moyenne_red = sum(rouge_trouve) // len(rouge_trouve)
        #print("Moyenne rouge: ", moyenne_red-w//2)
    else:
        moyenne_red=10000

    #moyenne jaune
    for y in range(5):
        for x in range(w):
            b, g, r = result_yellow[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                jaune_trouve.append(x)
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_yellow[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                jaune_trouve.append(x)
    for y in range(h-5,h):
        for x in range(w):
            b, g, r = result_yellow[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                jaune_trouve.append(x)
    if(len(jaune_trouve)!=0):
        moyenne_yellow = sum(jaune_trouve) // len(jaune_trouve)
        #print("Moyenne jaune: ", moyenne_yellow-w//2)
    else:
        moyenne_yellow=10000

    #comptage marron
    for y in range(h//2,h//2+5):
        for x in range(w):
            b, g, r = result_brown[y, x]
            if r!=0:
                marron_trouve += 1

    return [moyenne_blue-w//2, moyenne_red-w//2, moyenne_yellow-w//2, marron_trouve]

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
    marron_trouve=0

    h, w, c = result_blue.shape

    #moyenne bleu
    for y in range(h):
        for x in range(w):
            b, g, r = result_blue[y, x]
            #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if b!=0:
                bleu_trouve.append(x)
    if(len(bleu_trouve)!=0):
        moyenne_blue = np.median(bleu_trouve)
        #moyenne_blue = sum(bleu_trouve) // len(bleu_trouve)-w//2
        #print("Moyenne bleu: ", moyenne_blue-w//2)
    else:
        moyenne_blue=10000

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
        moyenne_red=10000

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
        moyenne_yellow=10000

    #comptage marron
    for y in range(h):
        for x in range(w):
            b, g, r = result_brown[y, x]
            if r!=0:
                marron_trouve += 1

    return [moyenne_blue, moyenne_red, moyenne_yellow, marron_trouve]
