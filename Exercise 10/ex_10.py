# ¿QUÉ HACE ESTE SCRIPT?
# Este script enciende la cámara de la PC y al detectar un AruCo
# de 6x6 y tamaño 250 con ids permitidos, se muestra un video sobre
# el mismo fiducial
# ---------------------------------------------------------------

import cv2
import numpy as np

# ---------------------------------------------------------------


video_name = "video.mp4"

# Allowed AruCos: "6x6 250"
allowed_ids = [1 , 2]

# ---------------------------------------------------------------


# The dictionary is loaded
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
# The detector is created
parameters = cv2.aruco.DetectorParameters_create()

dest_pts = []
dest_pts = np.asarray(dest_pts)

# ---------------------------------------------------------------


def rectifyImage(frame_cam, frame_vid, src_pts, dest_pts):
	# The image is rectified
	M = cv2.getPerspectiveTransform(src_pts, dest_pts)
	rectifiedImage = cv2.warpPerspective(frame_vid, M, (frame_cam.shape[1], frame_cam.shape[0]))
	return rectifiedImage
	
# ---------------------------------------------------------------


# Camera Video Parameters
cap_cam = cv2.VideoCapture(0)
width_cam = int(cap_cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height_cam = int(cap_cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_cam = int(cap_cam.get(cv2.CAP_PROP_FPS))
#print("width_cam: " + str(width_cam) + "   height_cam: " + str(height_cam) + "   fps_cam: " + str(fps_cam))

# Video Parameters
cap_vid = cv2.VideoCapture(video_name)
width_vid = int(cap_vid.get(cv2.CAP_PROP_FRAME_WIDTH))
height_vid = int(cap_vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps_vid = int(cap_vid.get(cv2.CAP_PROP_FPS))
#print("width_vid: " + str(width_vid) + "   height_vid: " + str(height_vid) + "   fps_vid: " + str(fps_vid))

src_pts = [[0 ,0], [width_vid-1, 0], [0, height_vid-1], [width_vid-1, height_vid-1]]
src_pts = np.asarray(src_pts, np.float32)

# ---------------------------------------------------------------


while(cap_cam.isOpened() and cap_vid.isOpened()):

	ret_cam, frame_cam = cap_cam.read()
	if ret_cam is True:
		# The markers are detected on the image
		corners, ids, rejected = cv2.aruco.detectMarkers(frame_cam, dictionary, parameters=parameters)
		if not(ids is None) and any(x in ids for x in allowed_ids):
			# If the detected AruCo's id is allowed 
			if len(corners):
				# If AruCos are detected
				dest_pts = [corners[0][0][0], corners[0][0][1], corners[0][0][3], corners[0][0][2]]
				dest_pts = np.asarray(dest_pts, np.float32)
				
				# A mask is created
				mask = np.ones((frame_cam.shape[0], frame_cam.shape[1], 3)) * 255
				contours = np.array([corners[0][0][0], corners[0][0][1], corners[0][0][2], corners[0][0][3]])
				contours = np.asarray(contours, np.int32)
				cv2.fillPoly(mask, pts = [contours], color=(0,0,0))
			else:
				# If AruCos are not detected
				mask = np.ones((frame_cam.shape[0], frame_cam.shape[1], 3)) * 255
				
			# The detected markers are drawn on the image
			#frame_cam = cv2.aruco.drawDetectedMarkers(frame_cam, corners, ids)
			#cv2.imshow('Animation', frame_cam)
			
			# A mask is applied to the camera frame, where the AruCo is
			frame_cam = np.multiply(frame_cam, np.where(mask == 0, 0, 1)).astype(np.float32)	
	else:
		break	
	
		
	ret_vid, frame_vid = cap_vid.read()
	if ret_vid is True:
		cv2.resizeWindow('Video', width_vid, height_vid)
	else:
		# The video restarts
		cap_vid = cv2.VideoCapture(video_name)
		continue
	
	# If AruCos are detected
	if len(corners) and not(ids is None) and any(x in ids for x in allowed_ids):
		# The video frame is rectified
		rectifiedImage = rectifyImage(frame_cam, frame_vid, src_pts, dest_pts).astype(np.float32)
		
		# The video frame is overlayed on to the camera frame
		cv2.imshow("Animation", cv2.add(frame_cam, rectifiedImage).astype(np.uint8))
	else:
		# No video frame is overlayed on to the camera frame
		cv2.imshow("Animation", frame_cam.astype(np.uint8))
		
	if (cv2.waitKey(1000//fps_vid) & 0xFF) == ord('q'):
		break
	
cap_cam.release()
cv2.destroyAllWindows()
