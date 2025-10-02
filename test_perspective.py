import cv2
import numpy as np
import sys

#Calibrage

def manual_perspective_transform(image, pts1, pts2):
    width, height = 300, 300
    img = image
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result


pts1 = np.float32([(14, 416), (620, 406), (538, 64), (80, 71)])
pts2 = np.float32([[0,0],[300,0],[300,300],[0,300]])

#Stitching

def stitch_images(images):
    imgs = []
    for img_name in images:
        img = cv2.imread(cv2.samples.findFile(img_name))
        cv2.imshow("Image", img)
        cv2.waitKey(0)   # attendre une touche
        img = manual_perspective_transform(img, pts1, pts2)
        cv2.imshow("Image", img)
        cv2.waitKey(0)   # attendre une touche
        if img is None:
            print("can't read image " + img_name)
            sys.exit(-1)
        imgs.append(img)
 
    #![stitching]
    stitcher = cv2.Stitcher.create(cv2.Stitcher_SCANS)
    status, res = stitcher.stitch(imgs)
 
    if status != cv2.Stitcher_OK:
        print("Can't stitch images, error code = %d" % status)
        sys.exit(-1)

    #![stitching]
    cv2.imwrite("image_final.jpg", res)

stitch_images(["images/image"+str(i)+".jpg" for i in range(1,100)])
#stitch_images(["reference.jpg"])