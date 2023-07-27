import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins connected to the servo(s)
servo_pin = 13 # Replace with the actual GPIO pins you are using

# Set up the GPIO pins as outputs
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(2.5)

# Function to move the MG996R servo to a specific angle
def move_servo():
    global time_passed
    time_passed = time.time()
    pwm.ChangeDutyCycle(12.5)
    
    while True:
        if time.time()-time_passed > 3:
            pwm.ChangeDutyCycle(2.5)
            break


move_servo()
''''
# Main code
if __name__ == "__main__":
    try:
        while True:
            # Move the first MG996R servo to 0 degrees
            move_mg996r_servo(servo_pins[0], 90)
            time.sleep(1)
             # Move the first MG996R servo to 0 degrees
            move_mg996r_servo(servo_pins[1], 90)
            time.sleep(1)

           

    except KeyboardInterrupt:
        # Clean up on Ctrl+C
        GPIO.cleanup()
'''