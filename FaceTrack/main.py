# This script will detect faces via your webcam.
# Tested with OpenCV3

import cv2

cap = cv2.VideoCapture(0)

# Create the haar cascade
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

midPoint = (-1,-1)

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	# Our operations on the frame come here
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5,
		minSize=(30, 30)
		#flags = cv2.CV_HAAR_SCALE_IMAGE
	)

	print("Found {0} faces!".format(len(faces)))
	cv2.putText(frame, "Faces found: {}".format(len(faces)), (5, 50),
				cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 0, 0), 1, cv2.LINE_AA)

	# Draw a rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		if(midPoint != (-1,-1)):
			cv2.line(frame, (midPoint), (int(x+w/2),midPoint[1]), (255, 0, 0), 1)
			cv2.line(frame, (int(x+w/2),midPoint[1]), (int(x+w/2),int(y+h/2)), (0, 0, 255), 1)
			cv2.putText(frame, "X offset: {}".format(int(x+w/2)-midPoint[0]),(5,20),
						cv2.FONT_HERSHEY_SIMPLEX, .3, (0,0,0), 1, cv2.LINE_AA)
			cv2.putText(frame, "Y offset: {}".format(-1*(int(y+h/2)-midPoint[1])),(5,30),
						cv2.FONT_HERSHEY_SIMPLEX, .3, (0,0,0), 1, cv2.LINE_AA)
			cv2.putText(frame, "Square size: {}".format(w*h),(5,40),
						cv2.FONT_HERSHEY_SIMPLEX, .3, (0,0,0), 1, cv2.LINE_AA)


	# Display the resulting frame
	cv2.imshow('frame', frame)

	midPoint = int(cv2.getWindowImageRect('frame')[2]/2),int(cv2.getWindowImageRect('frame')[3]/2)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()