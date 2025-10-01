import cv2
import numpy as np
import sys

#Calibrage

def manual_perspective_transform(image, pts1, pts2):
    width, height = 300, 300
    img = cv2.imread("image_test.jpg")
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    cv2.imwrite("output.jpg", result)


def correction_angle(image, angle_deg, focal_length=800):
    h, w = image.shape[:2]
    angle = np.deg2rad(angle_deg)

    # Matrice de projection perspective
    A1 = np.array([[1,0,-w/2],
                   [0,1,-h/2],
                   [0,0,1]])
    
    RX = np.array([[1,0,0],
                   [0,np.cos(angle),-np.sin(angle)],
                   [0,np.sin(angle), np.cos(angle)]])
    
    T = np.array([[focal_length,0,w/2],
                  [0,focal_length,h/2],
                  [0,0,1]])
    
    H = T @ RX @ A1
    img_corr = cv2.warpPerspective(image, H, (w,h))
    return img_corr


pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]])
pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

#Stitching

def stitch_images(images):
    imgs = []
    for img_name in images:
        img = cv2.imread(cv2.samples.findFile(img_name))
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