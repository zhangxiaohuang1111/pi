import RPi.GPIO as GPIO
import time

# GPIO Pin Setup for ECE 5725:
PWMA = 16  # Motor A PWM Pin
AIN1 = 5   # Motor A Direction Pin 1
AIN2 = 6   # Motor A Direction Pin 2

# Initialize GPIO pins for motor control
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)   # PWM Pin
GPIO.setup(AIN1, GPIO.OUT)   # Motor A direction control
GPIO.setup(AIN2, GPIO.OUT)

# Set up PWM for motor speed control
pwm_a = GPIO.PWM(PWMA, 50)  # Set PWM to 50Hz
pwm_a.start(0)              # Start with motor stopped (0% duty cycle)

def motor_stop():
    """Stop the motor"""
    pwm_a.ChangeDutyCycle(0)
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    print("Motor stopped")

def motor_forward(speed):
    """Move motor forward (clockwise) at the given speed (0-100%)"""
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(speed)
    print(f"Motor forward at {speed}% speed")

def motor_backward(speed):
    """Move motor backward (counterclockwise) at the given speed (0-100%)"""
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(speed)
    print(f"Motor backward at {speed}% speed")

try:
    # Start with the motor stopped
    motor_stop()
    time.sleep(1)
    
    # Range motor speed in the clockwise direction
    print("Ranging motor speed forward (clockwise)...")
    motor_forward(50)  # Half speed
    time.sleep(3)
    
    motor_forward(100)  # Full speed
    time.sleep(3)
    
    motor_stop()  # Stop motor
    time.sleep(1)
    
    # Range motor speed in the counterclockwise direction
    print("Ranging motor speed backward (counterclockwise)...")
    motor_backward(50)  # Half speed
    time.sleep(3)
    
    motor_backward(100)  # Full speed
    time.sleep(3)
    
    motor_stop()  # Stop motor again
    time.sleep(1)
    
except KeyboardInterrupt:
    print("Program interrupted by user")
    
finally:
    # Cleanup GPIO
    pwm_a.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")