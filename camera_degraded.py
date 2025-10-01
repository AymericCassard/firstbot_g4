import numpy as np
import cv2



img = cv2.imread("C:/Users/anton/Documents/ENSEIRB/s9/robot1/photos/finpiste1.png")
cv2.imshow('image1',img)

small = cv2.resize(img, (0,0), fx=0.10, fy=0.10, interpolation=cv2.INTER_AREA)
cv2.imwrite("compressed.jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 20])
degraded = cv2.imread("compressed.jpg")
cv2.imshow("Image compressée", degraded)

hsv = cv2.cvtColor(degraded, cv2.COLOR_BGR2HSV)
lower_blue = np.array([100, 100, 50])
upper_blue = np.array([140, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
result = cv2.bitwise_and(degraded, degraded, mask=mask)

himg, wimg, cimg = img.shape
hdegraded, wdegraded, cdegraded = degraded.shape
hresult, wresult, cresult = result.shape

print(himg,wimg,hdegraded,wdegraded,hresult,wresult)

bleu_trouve=[]

h, w, c = result.shape
for y in range(h):
    for x in range(w):
        b, g, r = result[y, x]   # Attention : ordre BGR
        #print(f"Pixel ({x},{y}) = Bleu:{b}, Vert:{g}, Rouge:{r}")
        if b!=0:
            bleu_trouve.append(x)

moyenne = sum(bleu_trouve) / len(bleu_trouve)
print(moyenne)

cv2.imshow('result',result)

cv2.waitKey(0)
cv2.destroyAllWindows()

