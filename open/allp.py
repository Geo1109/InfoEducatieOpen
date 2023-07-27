import cv2
import face_recognition

# Create a video capture object
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video capture
    ret, frame = cap.read()

    # Convert the frame to RGB format for face_recognition
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations in the frame
    face_locations = face_recognition.face_locations(rgb_frame)

    # Draw rectangles around the detected faces
    for face_location in face_locations:
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Display the frame
    cv2.imshow('Face Detection', frame)

    # Check for user input to quit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
