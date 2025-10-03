import time
import turtle
import cv2
import numpy as np
import manipulation_image
import math

height, width = 5000, 5000
#conversion pixel <--> m
# 300 x 300 => 125 mm * 125 mm
pixel_to_mm = 125/300
mm_to_pixel = 1/pixel_to_mm
l = 160 #160

f = open("positions.txt", "r")
coos = []
for line in f.readlines():
    x_str, y_str, theta_str = line.strip().split(",")
    x, y, theta = float(x_str), float(y_str), float(theta_str)
    x, y = x*1000, y*1000  # conversion en mm
    coos.append((x, y, theta))

images_link = ["images/image"+str(i)+".jpg" for i in range(1, len(coos)+1)]
images = [cv2.imread(image) for image in images_link] 
images = [manipulation_image.manual_perspective_transform(image) for image in images]
images = [cv2.cvtColor(image, cv2.COLOR_BGR2BGRA) for image in images]


def rotate_good(image, theta):
    # Centre et matrice de rotation
    (h, w) = image.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), theta, 1.0) #theta sens horaire

    # Rotation (la taille reste la même, coins coupés possible)
    rotated = cv2.warpAffine(image, M, (w, h), borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0))
    return rotated


def coo_to_reel_coo(x, y, t):
    return x + l*np.cos(t), y + l*np.sin(t), t

def paste(img, canva, x_center, y_center):
    x = int(x_center) - 150
    y = int(y_center) - 150
    h, w = img.shape[:2]
    for i in range(h):
        for j in range(w):
            if img[i, j][3] != 0:   # si le pixel n'est pas transparent
                if 0 <= y+i < height and 0 <= x+j < width:
                    canva[y+i, x+j] = img[i, j][:3]
    return canva


def image_to_pixel():
    canva = np.ones((height, width, 3), dtype=np.uint8) * 255
    for i, (image, (x, y, theta)) in enumerate(zip(images, coos)):
        print("theta :",theta/np.pi*180)
        if i > 0 :
            vx = coos[i][0] - coos[i-1][0]
            vy = coos[i][1] - coos[i-1][1]
            theta = math.atan2(vy, vx)
        print("estimation theta:", theta/np.pi*180)
        if i%1 == 0:
            print(f"Image {i+1}/{len(images)}")
            image  = rotate_good(image, theta*180/np.pi)
            cv2.imshow("Image", image)
            cv2.waitKey(200)
            x, y, theta = coo_to_reel_coo(x, y, theta)
            x_robot_pixel = x * mm_to_pixel
            y_robot_pixel = y * mm_to_pixel
            #print("x_robot_pixel:", x_robot_pixel, "y_robot_pixel:", y_robot_pixel)
            canva = paste(image, canva, x_robot_pixel + width//2, height//2 - y_robot_pixel)

    canva_small = cv2.resize(canva, (1000, 1000), interpolation=cv2.INTER_AREA)
    cv2.imshow("Canva", canva_small)
    cv2.waitKey(100)

image_to_pixel()
cv2.waitKey(0)
cv2.destroyAllWindows()

        