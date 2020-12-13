import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('/home/zeta/Videos/provaVLC2.mp4')

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:

# Real time stream
	a = 229; #y1
	b = 288; #y2
	c = 198; #x1
	d = 306; #x2

# Debug video provaVLC2.mp4
#	a = 365; #y1
#	b = 500; #y2
#	c = 765; #x1
#	d = 970; #x2


	ret, frame = cap.read()
	
	roi = frame[a: b, c: d];

	rows, cols, _ = roi.shape
	gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
	gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)


	# Get dark areas
	_, threshold = cv2.threshold(gray_roi, 70, 255, cv2.THRESH_BINARY_INV)
	# Questo mi ha fatto impazzire per ore, `_` e' usato per ignorare valori
	# che non servono durante l'unpacking, ma findContours ne ritorna solo 2
	contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#	if contours:
	contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)


#	if False:
	for cnt in contours:
		(x, y, w, h) = cv2.boundingRect(cnt)
		#cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
		cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
		cv2.line(roi, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
		cv2.line(roi, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)

		# coordinate of center of pupils
		print(x+int(w/2), "\t", y+int(h/2))

		break




	# Rotate stuff
#	frame = cv2.rotate(frame, cv2.ROTATE_180)
	roi = cv2.rotate(roi, cv2.ROTATE_180)
	gray_roi = cv2.rotate(gray_roi, cv2.ROTATE_180)
	threshold = cv2.rotate(threshold, cv2.ROTATE_180)

	cv2.imshow('Contours', roi)
	cv2.imshow("Threshold", threshold)
#	cv2.imshow('Input', frame)
	cv2.imshow('Eyes', gray_roi)

	c = cv2.waitKey(1)

	if c == 64:
		a += 1
		print("Yes")

	if c == 27:
		break

cap.release()
cv2.destroyAllWindows()
