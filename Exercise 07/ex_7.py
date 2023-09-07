import cv2
import numpy as np

# ------------------------------------------------------------

red = (0, 0, 255)
xybutton_down = 0, 0
dest_pts = [[0, 0], [0, 0], [0, 0]]
i = 0

#-------------------------------------------------------------

def selectPoint(event, x, y, flags, param):
	global xybutton_down, dest_pts, i
	if event == cv2.EVENT_LBUTTONDOWN and i < 3:
		xybutton_down = x, y
		cv2.circle(img2, (x, y), 4, red, -1)
		dest_pts[i] = xybutton_down
		i = i + 1
        
def affineTransform(img1, src_pts, dest_pts, size): 
	# Se computa la matriz de transfromación y se computa la transformación
	M = cv2.getAffineTransform(src_pts, dest_pts) 
	transf_img1 = cv2.warpAffine(img1, M, size, borderValue=(255,255,255)) 
	mask = cv2.warpAffine(img1, M, size, borderValue=(0,255,0))
	
	return transf_img1, mask
	
def embedImage(img1, img2, src_pts, dest_pts):
	img2 = img2_original.copy()
	
	# Se llama a la función que computa la transformación afín
	size = (img2.shape[1], img2.shape[0])
	transf_img1, mask = affineTransform(img1, src_pts, dest_pts, size)
	
	# Se incrusta la imagen 1 en 2
	for y in range(img2.shape[0]):
		for x in range (img2.shape[1]):
			if(not(mask[y, x, 0] == 0 and mask[y, x, 1] == 255 and mask[y, x, 2] == 0)):
				img2[y, x, :] = transf_img1[y, x, :]
	return img2
 
# ------------------------------------------------------------

# Se lee la imagen que se incrustará en la otra y se determinan
# los puntos origen
img1 = cv2.imread("image1.jpg", 1) 
src_pts = [[0 ,0], [img1.shape[1]-1, 0], [0, img1.shape[0]-1]]
src_pts = np.asarray(src_pts)

# Se lee la imagen a la cual se le incrustará la otra
img2 = cv2.imread("image2.jpg", 1) 
img2_original = img2.copy()

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', selectPoint)

while(1):
    cv2.imshow('Image', img2)
    
    k = cv2.waitKey(10) & 0xFF
    
    if k == 27:
    	# Se presiona Esc
        break	
        
    elif k == ord('r'):
    	# Se restaura la imagen de fondo
    	img2 = img2_original.copy()
    	i = 0
    
    elif k == ord('a'):
    	# Se incrusta la imagen
    	img2 = embedImage(img1, img2, np.float32(src_pts), np.float32(dest_pts))
    	
cv2.destroyAllWindows()
