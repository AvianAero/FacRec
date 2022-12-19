# This script will detect faces via your webcam.
# Tested with OpenCV3

import cv2

# Distance from camera to face (in)
Known_distance = 30

# Width of face (in)
Known_width = 6

# Colors
GREEN = (0, 255, 0)
RED = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


midPoint = (-1,-1)

# Define default font
fonts = cv2.FONT_HERSHEY_SIMPLEX

# Object to detect face
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# Function to find focal length of camera
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):

    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# Distance estimator
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance = (real_face_width * Focal_Length) / face_width_in_frame

    return distance


def face_data(image):
    face_width = 0

    # Convert image to gray scale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect face in image
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    # Getting coordinates for faces
    for (x, y, h, w) in faces:
        # Draw a rectangle on the face
        cv2.rectangle(image, (x, y), (x + w, y + h), GREEN, 2)

        if (midPoint != (-1, -1)):
            cv2.line(frame, (midPoint), (int(x + w / 2), midPoint[1]), (255, 0, 0), 1)
            cv2.line(frame, (int(x + w / 2), midPoint[1]), (int(x + w / 2), int(y + h / 2)), (0, 0, 255), 1)
            cv2.putText(frame, "X offset: {}".format(int(x + w / 2) - midPoint[0]), (5, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, "Y offset: {}".format(-1 * (int(y + h / 2) - midPoint[1])), (5, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, "Square size: {}".format(w * h), (5, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, .3, (0, 0, 0), 1, cv2.LINE_AA)

        # Get face width in pixels
        face_width = w

    return face_width


# Read Reference Image
ref_image = cv2.imread("Ref_image.png")

# Get reference face width
ref_image_face_width = face_data(ref_image)

Focal_length_found = Focal_Length_Finder(
    Known_distance, Known_width, ref_image_face_width)

print(Focal_length_found)

# Initialize camera
cap = cv2.VideoCapture(0)

while True:

    _, frame = cap.read()

    face_width_in_frame = face_data(frame)

    if face_width_in_frame != 0:

        Distance = Distance_finder(
            Focal_length_found, Known_width, face_width_in_frame)


        cv2.putText(
            frame, f"Distance: {round(Distance, 2)} IN", (10
                                                          , 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, BLACK, 1)

    # Show the camera
    cv2.imshow("frame", frame)

    midPoint = int(cv2.getWindowImageRect('frame')[2] / 2), int(cv2.getWindowImageRect('frame')[3] / 2)

    # Quit the program if you press 'q' on keyboard
    if cv2.waitKey(1) == ord("q"):
        break

# Stop recording
cap.release()

# Close all windows
cv2.destroyAllWindows()