import cv2

img = cv2.imread('lena.jpg', 1)
###
# img = cv2.arrowedLine(img, (0,0), (240,240), (0,0,255), 5)
img = cv2.rectangle(img, (200,200), (355,355), (0,0,255),5)
img = cv2.circle
###
winshow = cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyWindow(winshow)

print(img)