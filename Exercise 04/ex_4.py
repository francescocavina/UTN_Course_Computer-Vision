import cv2
import numpy as np

blue = (255, 0, 0); green = (0, 255, 0); red = (0, 0, 255)
drawing = False
xybutton_down = -1, -1
xy_end = -1, -1

def dibuja(event, x, y, flags, param):
    global xybutton_down, xy_end, drawing, img
    xy_end = x, y

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        xybutton_down = x, y 
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True:
            img = cv2.imread('image.jpg', 1)
            cv2.rectangle(img, xybutton_down, (x, y), red, 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

img = cv2.imread('image.jpg', 1)
cv2.namedWindow('image')
cv2.setMouseCallback('image', dibuja)

while(1):
    cv2.imshow('image', img)
    k = cv2.waitKey(10) & 0xFF
    if k == ord('g'):
        h, w, c = img.shape
        h_min = min(xybutton_down[1], xy_end[1])
        h_max = max(xybutton_down[1], xy_end[1])
        w_min = min(xybutton_down[0], xy_end[0])
        w_max = max(xybutton_down[0], xy_end[0])
        edited_image = cv2.imread('image.jpg', 1)[h_min:h_max, w_min:w_max, :]
        cv2.imwrite('edited_image.jpg', edited_image)
        break
    elif k == ord('r'):
        img = cv2.imread('image.jpg', 1)
    elif k == ord('q'):
        break

cv2.destroyAllWindows()
