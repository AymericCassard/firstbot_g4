import cv2

points = []

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:   # clic gauche
        points.append((x, y))
        print("Point:", (x, y))

img = cv2.imread("reference.jpg")
cv2.imshow("Image", img)
cv2.setMouseCallback("Image", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()
print("Tous les points:", points)
