import cv2
import numpy as np
import math

def similarity(img, angle, tx, ty, s):
    h, w, c  = img.shape
    
    angle_rad = math.radians(angle)

    transf_img = np.zeros(img.shape, np.uint8)

    for i in range(transf_img.shape[0]):
        for j in range(transf_img.shape[1]):
        
            x = j * s * math.cos(angle_rad) + i * s * math.sin(angle_rad) + tx
            y = -j * s * math.sin(angle_rad) + i * s * math.cos(angle_rad) + ty

            x = round(x)
            y = round(y)

            if(x >= 0 and y >= 0 and x < w and y < h):
                # Lo siguiente se hace porque al escalar, existen píxeles que quedarían vacíos
                if(s > 1):
                    for a in range(math.ceil(y-s), y+1):
                        for b in range(math.ceil(x-s), x+1):
                            transf_img[a, b, :] = img[i, j, :]
                elif(s <= 1):
                    transf_img[y, x, :] = img[i, j, :]

    return transf_img

img = cv2.imread('image_a.jpg', 1)
transf_img = similarity(img, 0, 0, 0, 2)
cv2.imshow('Original Image', img)
cv2.imshow('Transformed Image', transf_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
