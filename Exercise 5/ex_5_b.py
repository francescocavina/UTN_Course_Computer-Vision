import cv2
import numpy as np
import math

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
            img = cv2.imread('image_b.jpg', 1)
            cv2.rectangle(img, xybutton_down, (x, y), red, 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

def euclidean(img, angle, tx, ty):
    h, w, c  = img.shape
    
    angle_rad = math.radians(angle)

    transf_img = np.zeros(img.shape, np.uint8)

    for i in range(transf_img.shape[0]):
        for j in range(transf_img.shape[1]):
        
            x = j * math.cos(angle_rad) - i * math.sin(angle_rad) - tx
            y = j * math.sin(angle_rad) + i * math.cos(angle_rad) - ty

            x = round(x)
            y = round(y)

            if(x >= 0 and y >= 0 and x < w and y < h):
                transf_img[i, j, :] = img[y, x, :]

    return transf_img


img = cv2.imread('image_b.jpg', 1)
cv2.namedWindow('Original Image')
cv2.setMouseCallback('Original Image', dibuja)

while(1):
    cv2.imshow('Original Image', img)
    k = cv2.waitKey(10) & 0xFF
    if k == ord('e'):
        h, w, c = img.shape
        h_min = min(xybutton_down[1], xy_end[1])
        h_max = max(xybutton_down[1], xy_end[1])
        w_min = min(xybutton_down[0], xy_end[0])
        w_max = max(xybutton_down[0], xy_end[0])
        edited_image = cv2.imread('image_b.jpg', 1)[h_min:h_max, w_min:w_max, :]
        cv2.imwrite('edited_image.jpg', euclidean(edited_image, 0, 50, 50))
        break
    elif k == ord('r'):
        img = cv2.imread('image_b.jpg', 1)
    elif k == ord('q'):
        break

cv2.destroyAllWindows()
