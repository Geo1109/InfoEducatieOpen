import cv2
import numpy as np
from scipy.spatial import distance as dist
from scipy.optimize import linear_sum_assignment

def detect_human_faces():
    # Load the pre-trained face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Open the default camera (usually 0)
    cap = cv2.VideoCapture(0)

    # List to store tracked persons and their labels
    tracked_persons = []

    # Counter to assign labels to new persons
    label_counter = 1

    while True:
        # Capture each frame from the camera
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to grayscale for face detection
        gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around the detected faces and label them
        for (x, y, w, h) in faces:
            # Calculate the centroid of the detected face
            centroid_x = x + w // 2
            centroid_y = y + h // 2

            # Use the Hungarian algorithm to match detected faces to existing tracked faces
            if len(tracked_persons) > 0:
                existing_centroids = np.array([(person[0] + person[2] // 2, person[1] + person[3] // 2) for person in tracked_persons])
                detected_centroid = np.array([(centroid_x, centroid_y)])
                cost_matrix = dist.cdist(existing_centroids, detected_centroid)
                row_ind, col_ind = linear_sum_assignment(cost_matrix)
                matched_indices = col_ind[row_ind == np.arange(len(row_ind))]
                is_tracked = len(matched_indices) > 0
            else:
                is_tracked = False

            if is_tracked:
                # This person is already being tracked, update the rectangle
                person_idx = row_ind[matched_indices[0]]
                tracked_persons[person_idx][:4] = [x, y, w, h]
            else:
                # This is a new person, assign a label and track them
                tracked_persons.append([x, y, w, h, label_counter])
                label_counter += 1

            # Draw rectangle around the face and label with person's number
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, str(tracked_persons[-1][4]), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Display the frame with detected faces and labels
        cv2.imshow('Real-Time Face Detection', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_human_faces()
