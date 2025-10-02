import cv2 as cv2
import numpy as np

# webcam = cv2.VideoCapture(0)
# ret, frame = webcam.read()
# small = cv2.resize(frame, (0,0), fx=0.10, fy=0.10, interpolation=cv2.INTER_AREA)
# cv2.imwrite("photo.jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 20])

def moyenne_couleurs(img):
    # small = img
    # degraded = cv2.imread("photo.jpg")
    small = cv2.resize(img, (0,0), fx=0.10, fy=0.10, interpolation=cv2.INTER_AREA)
    cv2.imwrite("compressed.jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 20])
    degraded = cv2.imread("compressed.jpg")
    # #cv2.imshow("Image compressée", degraded)

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
    #OLD
    lower_brown1 = np.array([160, 40, 40])
    upper_brown1 = np.array([179, 150, 150])
    lower_brown2 = np.array([0, 40, 40])
    upper_brown2 = np.array([20, 150, 150])
    mask_brown1 = cv2.inRange(hsv, lower_brown1, upper_brown1)
    mask_brown2 = cv2.inRange(hsv, lower_brown2, upper_brown2)
    mask_brown = cv2.bitwise_or(mask_brown1, mask_brown2)

    # lower_brown1 = np.array([160, 30, 20])   # S et V abaissés pour inclure foncé/terne
    # upper_brown1 = np.array([179, 200, 180]) # S et V augmentés pour inclure clair/vif
    # lower_brown2 = np.array([0, 30, 20])
    # upper_brown2 = np.array([20, 200, 180])
    # mask_brown1 = cv2.inRange(hsv, lower_brown1, upper_brown1)
    # mask_brown2 = cv2.inRange(hsv, lower_brown2, upper_brown2)
    # mask_brown = cv2.bitwise_or(mask_brown1, mask_brown2)

    result_brown = cv2.bitwise_and(degraded, degraded, mask=mask_brown)

    jaune_trouve=[]
    rouge_trouve=[]
    bleu_trouve=[]
    marron_trouve=[]

    h, w, c = result_blue.shape
    cv2.imshow("original", img)
    cv2.imshow("masque bleu", mask_blue)
    cv2.imshow("masque marron", mask_brown)

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


    k = cv2.waitKey(0)
    #comptage marron
    for y in range(h):
        for x in range(w):
            b, g, r = result_brown[y, x]
            # print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
            if r!=0:
                marron_trouve.append(x)

    print(f"nbjaune trouve: {len(jaune_trouve)}")
    print(f"nbbleu trouve: {len(bleu_trouve)}")
    print(f"nbrouge trouve: {len(rouge_trouve)}")
    print(f"nbmarron trouve: {len(marron_trouve)}")

    return [moyenne_blue, moyenne_red, moyenne_yellow]

img = cv2.imread("photo.jpg")
# print(img[315][173])
test = moyenne_couleurs(img)
# cv2.imshow("Display window", img)
# k = cv2.waitKey(0)
# print(test)

