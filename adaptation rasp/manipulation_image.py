import cv2
import numpy as np
import sys

#Calibrage

def manual_perspective_transform(image, pts1 = np.float32([(18, 419), (90, 15), (521, 0), (620, 405)]), pts2 = np.float32([[0,0],[300,0],[300,300],[0,300]])):
    width, height = 300, 300
    img = image
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result

#Stitching

def stitch_images(images):
    imgs = []
    for img_name in images:
        img = cv2.imread(cv2.samples.findFile(img_name))
        img = manual_perspective_transform(img)
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

#stitch_images(["images/image"+str(i)+".jpg" for i in [25,45]])
#stitch_images(["reference.jpg"])