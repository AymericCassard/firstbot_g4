import numpy as np
import cv2

cap = cv2.VideoCapture(0)



while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #cv2.imwrite("C:/Users/anton/Documents/ENSEIRB/s9/robot1/messigray.png",frame)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    laplacian = cv.Laplacian(gray,cv.CV_64F)

    # Display the resulting frame
    cv2.imshow('frame',laplacian)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()