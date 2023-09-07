import sys
import cv2

if(len(sys.argv) > 1):
        filename = sys.argv[1]
else:
    print('Pasar el nombre del video como argumento')
    sys.exit(0)

cap = cv2.VideoCapture(filename)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == False:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

    cv2.imshow('frame', gray)
    cv2.resizeWindow('frame', width, height)
    if((cv2.waitKey(1000//fps) & 0xFF) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
