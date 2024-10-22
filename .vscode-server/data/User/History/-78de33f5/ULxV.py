import RPi.GPIO as GPIO
import time

# GPIO Pin Setup for Motor A and Motor B
AIN1 = 5  # Motor A Direction Pin 1
AIN2 = 6  # Motor A Direction Pin 2
BIN1 = 20 # Motor B Direction Pin 1
BIN2 = 21 # Motor B Direction Pin 2
PWMA = 16 # Motor A PWM Control (also used for Motor B)

# GPIO Pin Setup for Buttons
buttonA_control = 17  # Button to control left motor (clockwise/counterclockwise toggle)
buttonA_stop = 22     # Button to stop left motor
buttonB_control = 23  # Button to control right motor (clockwise/counterclockwise toggle)
buttonB_stop = 27     # Button to stop right motor
button_exit = 26      # Button to exit the program

# Setup GPIO mode and disable warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup GPIO pins for motors
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

# Setup GPIO pins for buttons
GPIO.setup(buttonA_control, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonA_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB_control, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize PWM for both motors (shared control)
pwm_a = GPIO.PWM(PWMA, 50)  # 50Hz PWM signal
pwm_a.start(0)  # Start with motor stopped

# State variables to track motor direction
stateA = 0  # 0 = stopped, 1 = clockwise, 2 = counterclockwise
stateB = 0  # 0 = stopped, 1 = clockwise, 2 = counterclockwise

# Motor A control functions
def motor_a_forward():
    """Set motor A to rotate clockwise at half speed."""
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)  # Set motor to half speed

def motor_a_backward():
    """Set motor A to rotate counterclockwise at half speed."""
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)

def motor_a_stop():
    """Stop motor A."""
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)

# Motor B control functions
def motor_b_forward():
    """Set motor B to rotate clockwise at half speed."""
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)

def motor_b_backward():
    """Set motor B to rotate counterclockwise at half speed."""
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)

def motor_b_stop():
    """Stop motor B."""
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)

# Button press event handlers
def handle_buttonA_control(channel):
    """Toggle motor A between clockwise and counterclockwise direction."""
    global stateA
    if stateA == 0 or stateA == 2:  # If stopped or counterclockwise, go clockwise
        motor_a_forward()
        print("Left motor forward (clockwise)")
        stateA = 1
    else:  # Switch to counterclockwise
        motor_a_backward()
        print("Left motor backward (counterclockwise)")
        stateA = 2

def handle_buttonA_stop(channel):
    """Stop motor A."""
    global stateA
    motor_a_stop()
    print("Left motor stopped")
    stateA = 0

def handle_buttonB_control(channel):
    """Toggle motor B between clockwise and counterclockwise direction."""
    global stateB
    if stateB == 0 or stateB == 2:  # If stopped or counterclockwise, go clockwise
        motor_b_forward()
        print("Right motor forward (clockwise)")
        stateB = 1
    else:  # Switch to counterclockwise
        motor_b_backward()
        print("Right motor backward (counterclockwise)")
        stateB = 2

def handle_buttonB_stop(channel):
    """Stop motor B."""
    global stateB
    motor_b_stop()
    print("Right motor stopped")
    stateB = 0

def handle_exit(channel):
    """Cleanly exit the program and stop all motors."""
    print("Exiting program...")
    pwm_a.stop()
    GPIO.cleanup()
    exit(0)

# Add event detection for button presses
GPIO.add_event_detect(buttonA_control, GPIO.FALLING, callback=handle_buttonA_control, bouncetime=300)
GPIO.add_event_detect(buttonA_stop, GPIO.FALLING, callback=handle_buttonA_stop, bouncetime=300)
GPIO.add_event_detect(buttonB_control, GPIO.FALLING, callback=handle_buttonB_control, bouncetime=300)
GPIO.add_event_detect(buttonB_stop, GPIO.FALLING, callback=handle_buttonB_stop, bouncetime=300)
GPIO.add_event_detect(button_exit, GPIO.FALLING, callback=handle_exit, bouncetime=300)

# Main loop to keep the program running
try:
    while True:
        time.sleep(0.1)  # Sleep to reduce CPU usage
except KeyboardInterrupt:
    print("Program interrupted by user")
finally:
    pwm_a.stop()
    GPIO.cleanup()