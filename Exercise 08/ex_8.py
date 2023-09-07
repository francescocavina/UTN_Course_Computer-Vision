import cv2
import numpy as np

# ------------------------------------------------------------

red = (0, 0, 255)
xybutton_down = 0, 0
src_pts = [[0, 0], [0, 0], [0, 0], [0, 0]]
i = 0

#-------------------------------------------------------------

def selectPoint(event, x, y, flags, param):
	global xybutton_down, dest_pts, i
	if event == cv2.EVENT_LBUTTONDOWN and i < 4:
		xybutton_down = x, y
		cv2.circle(img, (x, y), 4, red, -1)
		src_pts[i] = xybutton_down
		i = i + 1
	
def rectifyImage(img, src_pts, dest_pts):
	img = img_original.copy()
	M = cv2.getPerspectiveTransform(src_pts, dest_pts)
	rectifiedImage = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
	
	return rectifiedImage
 
# ------------------------------------------------------------

img = cv2.imread("image.jpg", 1) 
dest_pts = [[0 ,0], [img.shape[1]-1, 0], [0, img.shape[0]-1], [img.shape[1]-1, img.shape[0]-1]]
dest_pts = np.asarray(dest_pts)
img_original = img.copy()

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', selectPoint)

while(1):
    cv2.imshow('Image', img)
    
    k = cv2.waitKey(10) & 0xFF
    
    if k == 27:
    	# Se presiona Esc
        break	
        
    elif k == ord('r'):
    	# Se restaura la imagen de fondo
    	img = img_original.copy()
    	i = 0
    
    elif k == ord('h'):
    	# Se realiza la rectificación
    	src_pts = np.asarray(src_pts)
    	img = rectifyImage(img, np.float32(src_pts), np.float32(dest_pts))
    	
cv2.destroyAllWindows()
