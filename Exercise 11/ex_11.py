import numpy as np
import cv2

MIN_MATCH_COUNT = 25

# Se leen las imágenes
img1 = cv2.imread('img1.jpg')
img2 = cv2.imread('img2.jpg')

# Se inicia el Detector SIFT
sift = cv2.SIFT_create()

# Se buscan los Keypoints y se generan los Descriptores con SIFT
kp1 , des1 = sift.detectAndCompute(img1, None)
kp2 , des2 = sift.detectAndCompute(img2, None)

# Se crea el objeto BFMatcher
matcher = cv2.BFMatcher(cv2.NORM_L2)
# Se determina cuales son los Matches entre los Keypoints encontrados
matches = matcher.knnMatch(des1, des2, k=2)

# Se guardan los buenos Matches usando el test de razón de Lowe
good = []
for m, n in matches :
	if m.distance < 0.5 * n.distance:
		good.append(m)
		
if(len(good) > MIN_MATCH_COUNT):
	src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
	dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

# Se computa la homografía con RAN-SAC
H, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0) 
# Se aplica la transformación
wimg2 = cv2.warpPerspective(img2, H, (img1.shape[1], img1.shape[0]))

# Se mezclan ambas imágenes
alpha = 0.5
blend = np.array(wimg2 * alpha + img1 * (1 - alpha), dtype=np.uint8)

# Se muestra la imagen resultante
cv2.imshow('Image', blend)

# cv.drawMatchesKnn espera una lista de listas
good = [good]
# Se dibujan los mejores Matches
img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Se muestran los Matches
cv2.imshow('Matching', img3)
cv2.waitKey(0)
