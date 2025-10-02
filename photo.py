import cv2 as cv2

webcam = cv2.VideoCapture(0)
ret, frame = webcam.read()
# small = cv2.resize(frame, (0,0), fx=0.10, fy=0.10, interpolation=cv2.INTER_AREA)
# cv2.imwrite("photo.jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 20])
cv2.imwrite("photo.jpg", frame)
