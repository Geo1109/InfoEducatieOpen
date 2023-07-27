import cv2
import numpy as np

# Load a pre-trained face detector from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the image or start the webcam capture
image = cv2.imread('path_to_your_image.jpg')
# If using webcam, uncomment the following line:
# cap = cv2.VideoCapture(0)

while True:
    # If using webcam, uncomment the following two lines:
    # ret, image = cap.read()
    # if not ret:
    #     break

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Calculate the center point of the detected face
        center_x = x + w // 2
        center_y = y + h // 2

        # Draw a rectangle around the detected face
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Draw a circle at the center of the detected face
        cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)

        # Check if the center of the face is towards the upper part of the image
        if center_y < image.shape[0] // 2:
            cv2.putText(image, 'Front of Head', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            cv2.putText(image, 'Back of Head', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the image with annotations
    cv2.imshow('Head Detection', image)

    # If using webcam, comment the following line:
    break

    # If using webcam, uncomment the following two lines:
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release the video capture and close any open windows
# If using webcam, uncomment the following line:
# cap.release()

cv2.destroyAllWindows()