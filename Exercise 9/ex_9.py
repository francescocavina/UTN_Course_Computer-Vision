import cv2
import numpy as np
from os import system

# ------------------------------------------------------------

red = (0, 0, 255); green = (0, 255, 0); blue = (255, 0, 0)
xybutton_down = 0, 0
i = 0
transf_flag = 0 # Para habilitar la selección de puntos solo luego de haber transformado
door_pts = [(206, 461), (310, 459), (203, 729), (312, 714)]

src_pts = [[0,0], [0,0], [0,0], [0,0]]

#-------------------------------------------------------------

def selectPoints(event, x, y, flags, param):
	global xybutton_down, dest_pts, i, pixelDistance_pt1_pt2_m
	if event == cv2.EVENT_LBUTTONDOWN and i < 2 and transf_flag == 1:
		xybutton_down = x, y
		cv2.circle(img, (x, y), 5, blue, -1)
		src_pts[i] = xybutton_down
		i = i + 1
		
	if i == 2: 
		# Si se seleccionaron los dos puntos
		cv2.line(img, src_pts[0], src_pts[1], red, 3)
		distance = calculateDistance_px(src_pts[0], src_pts[1]) * pixelDistance_pt1_pt2_m
		distance = round(distance, 2)
		x_pos = (src_pts[1][0] - src_pts[0][0]) // 2 + src_pts[0][0] - 10
		y_pos = (src_pts[1][1] - src_pts[0][1]) // 2 + src_pts[0][1] - 10
		cv2.putText(img, str(distance) + "m", (x_pos, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, green, 2)
		i = 0	
    		
def rectifyImage(img, door_pts, dest_pts):
	# Se rectifica la imagen
	M = cv2.getPerspectiveTransform(door_pts, dest_pts)
	rectifiedImage = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
	return rectifiedImage
	
def drawImage():	
	cv2.line(img, door_pts[0], door_pts[1], red, 3)
	cv2.line(img, door_pts[2], door_pts[0], red, 3)
	cv2.circle(img, door_pts[0], 5, blue, -1)
	cv2.circle(img, door_pts[1], 5, blue, -1)
	cv2.circle(img, door_pts[2], 5, blue, -1)
	cv2.circle(img, door_pts[3], 5, blue, -1)
	cv2.putText(img, "0.82m", (237, 445), cv2.FONT_HERSHEY_SIMPLEX, 0.5, red, 2)
	cv2.putText(img, "2.1m", (152, 585), cv2.FONT_HERSHEY_SIMPLEX, 0.5, red, 2)

def calculateDistance_px(pointA, pointB): 
	# Retorna la distancia entre dos puntos, en pixeles
	distance_px = ((pointB[0] - pointA[0]) ** 2 + (pointB[1] - pointA[1]) ** 2) ** 0.5
	return distance_px 

# ------------------------------------------------------------

img = cv2.imread("image.jpg", 1) 
img_original = img.copy()
drawImage()

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', selectPoints)

door_width_px = calculateDistance_px(door_pts[0], door_pts[1])
door_height_px = calculateDistance_px(door_pts[0], door_pts[2])
dest_pts = [[door_pts[0][0], door_pts[0][1]], [door_pts[0][0]+door_width_px, door_pts[0][1]], [door_pts[0][0], door_pts[0][1]+door_height_px], [door_pts[0][0]+door_width_px, door_pts[0][1]+door_height_px]]
dest_pts_mx = np.asarray(dest_pts)

distance_pt1_pt2_px = calculateDistance_px(door_pts[0], door_pts[1])
pixelDistance_pt1_pt2_m = 0.82 / distance_pt1_pt2_px

system('clear')
print("- - - - - Trabajo Práctico N° 9 - - - - -\n") 
print("Presione sobre la imagen: ")
print("  - ESC para salir")
print("  - 'h' para rectificar")
print("  - 'r' para restaurar")
print("\nUna vez rectificada la imagen, seleccione \npares de puntos para medir la distancia")

while(1):
	cv2.imshow('Image', img)

	k = cv2.waitKey(10) & 0xFF

	if k == 27:
		# Se presiona Esc
		break	   
	elif k == ord('h'):
		# Se realiza la rectificación
		door_pts_mx = np.asarray(door_pts)
		if transf_flag == 0:
			img = rectifyImage(img, np.float32(door_pts_mx), np.float32(dest_pts_mx))
			transf_flag = 1
	elif k == ord('r'):
		# Se restaura la imagen
		transf_flag = 0 # No se pueden seleccionar puntos
		i = 0 # Se resetea el contador de puntos
		img = img_original.copy() # Se vuelve a la imagen original
		drawImage() 	
   
cv2.destroyAllWindows()
