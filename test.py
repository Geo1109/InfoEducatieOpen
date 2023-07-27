import os
import numpy as np
import argparse
import imutils
import cv2
from collections import deque

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64, help="max buffer size")
args = vars(ap.parse_args())

# Define the path to the folder for saving photos
output_folder = os.path.join(os.path.expanduser("~/Desktop"), "pozeopen")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# define the lower and upper boundaries of the "yellow object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, inverted ("vertical flip" w/ 180degrees)
    frame = imutils.resize(frame, width=600)

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define a mask to detect yellow color
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([40, 255, 255], dtype=np.uint8)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Apply Gaussian blur to the mask to reduce noise
    yellow_mask = cv2.GaussianBlur(yellow_mask, (9, 9), 0)

    # Find contours in the mask
    cnts = cv2.findContours(yellow_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # Only proceed if at least one contour was found
    if len(cnts) > 0:
        # Find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
        # Check if the contour area is greater than zero
        if cv2.contourArea(c) > 0:
            center = (int(x), int(y))
            # Only proceed if the radius meets a minimum size
            if radius > 10:
                # Draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, center, int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

                # Calculate the distance between the center of the object and the center of the screen
                screen_center_x = frame.shape[1] // 2
                screen_center_y = frame.shape[0] // 2
                distance_to_center = np.sqrt((center[0] - screen_center_x) ** 2 + (center[1] - screen_center_y) ** 2)
                print("Distance to center:", distance_to_center)

                # Take a photo if the distance is less than 20
                if distance_to_center < 5:
                    # Generate a unique filename for the photo
                    photo_filename = os.path.join(output_folder, "photo_{:04d}.jpg".format(len(os.listdir(output_folder))))
                    cv2.imwrite(photo_filename, frame)

    # Update the points queue
    pts.appendleft(center)

    # Loop over the set of tracked points
    for i in range(1, len(pts)):
        # If either of the tracked points are None, ignore them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # Otherwise, compute the thickness of the line and
        # draw the connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # Show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # If the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# Cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
