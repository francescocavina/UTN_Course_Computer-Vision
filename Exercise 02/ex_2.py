import cv2

img = cv2.imread('hojas.png', 0) 

threshold = 25

h, w = img.shape

for row in range(h):
    for col in range(w):
        if img[row, col] <= threshold:
            img[row, col] = 255
        else:
            img[row, col] = 0

cv2.imwrite('resultado.png', img)
