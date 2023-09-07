import cv2

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret is True:
        out.write(frame)
        cv2.imshow('frame', frame)
        if (cv2.waitKey(1000//fps) & 0xFF) == ord('q'):
            break
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
