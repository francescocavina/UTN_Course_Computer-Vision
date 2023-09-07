import cv2
import numpy as np
import math

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

img = cv2.imread('image_a.jpg', 1)
transf_img = euclidean(img, 0, 50, 50)
cv2.imshow('Original Image', img)
cv2.imshow('Transformed Image', transf_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
