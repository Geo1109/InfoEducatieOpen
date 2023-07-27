import cv2
import face_recognition
import RPi.GPIO as GPIO
import threading
import time

# Set up servo GPIO and PWM
GPIO.setmode(GPIO.BCM)
servo_pin = 13
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz PWM frequency
pwm.start(0)

# Variable to indicate if a person is detected
detected_person = False

# Function to set the angle of the servo motor
def set_angle(angle):
    duty_cycle = 2 + (angle / 18)  # Map angle (0 to 180) to duty cycle (2 to 12)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.3)  # Wait for the servo to move to the desired position

# Function for face recognition
def face_recognition_thread():
    global detected_person
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        # Convert the frame from BGR to RGB (face_recognition uses RGB format)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face locations in the frame
        face_locations = face_recognition.face_locations(rgb_frame)

        # Update the detected_person flag based on whether a person is detected
        detected_person = len(face_locations) > 0

        # Draw rectangles around the detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Face Recognition', frame)

        # Check for user input to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Create and start the face recognition thread
face_thread = threading.Thread(target=face_recognition_thread)
face_thread.start()

try:
    while True:
        # Move servo from 0 to 180 degrees if no person is detected
        if not detected_person:
            for angle in range(0, 181, 5):
                set_angle(angle)
                time.sleep(0.1)  # Add a slight delay to smooth the movement

        # Move servo from 180 to 0 degrees if a person is detected
        if detected_person:
            for angle in range(180, -1, -5):
                set_angle(angle)
                time.sleep(0.1)  # Add a slight delay to smooth the movement

except KeyboardInterrupt:
    # Clean up and stop PWM on Ctrl+C
    pwm.stop()
    GPIO.cleanup()
