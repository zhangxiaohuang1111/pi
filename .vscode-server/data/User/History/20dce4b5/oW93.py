import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *

# GPIO Pin Setup for Motors (Use your previously defined motor pins)
AIN1 = 5
AIN2 = 6
BIN1 = 20
BIN2 = 21
PWMA = 16

# Setup GPIO as in your original code...
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

# PWM setup
pwm_a = GPIO.PWM(PWMA, 50)  # 50Hz PWM signal
pwm_a.start(0)  # Start with motor stopped

# Motor state variables
stateA = 0  # 0 = stopped, 1 = clockwise, 2 = counterclockwise
stateB = 0
historyA = []
historyB = []

# Pygame setup for PiTFT display
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((320, 240))

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Button definitions
panic_button = pygame.Rect(20, 180, 130, 50)  # Button for panic/stop/resume
quit_button = pygame.Rect(170, 180, 130, 50)  # Quit button
motor_history_posA = [20, 20]  # Display position for motor A history
motor_history_posB = [170, 20]  # Display position for motor B history

# Variable to track panic state
panic_mode = False  # False = normal mode, True = panic mode

# Motor control functions (same as your original ones)
def motor_a_forward():
    """Set motor A to rotate clockwise at half speed."""
    global historyA
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    historyA.append((time.strftime("%H:%M:%S"), "clockwise"))
    if len(historyA) > 3:
        historyA.pop(0)

def motor_a_backward():
    """Set motor A to rotate counterclockwise at half speed."""
    global historyA
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)
    historyA.append((time.strftime("%H:%M:%S"), "counterclockwise"))
    if len(historyA) > 3:
        historyA.pop(0)

def motor_a_stop():
    """Stop motor A."""
    global historyA
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    historyA.append((time.strftime("%H:%M:%S"), "stopped"))
    if len(historyA) > 3:
        historyA.pop(0)

def motor_b_forward():
    """Set motor B to rotate clockwise at half speed."""
    global historyB
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    historyB.append((time.strftime("%H:%M:%S"), "clockwise"))
    if len(historyB) > 3:
        historyB.pop(0)

def motor_b_backward():
    """Set motor B to rotate counterclockwise at half speed."""
    global historyB
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)
    historyB.append((time.strftime("%H:%M:%S"), "counterclockwise"))
    if len(historyB) > 3:
        historyB.pop(0)

def motor_b_stop():
    """Stop motor B."""
    global historyB
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    historyB.append((time.strftime("%H:%M:%S"), "stopped"))
    if len(historyB) > 3:
        historyB.pop(0)

# Panic stop/resume button handler
def handle_panic_stop():
    global panic_mode
    if not panic_mode:
        motor_a_stop()
        motor_b_stop()
        panic_mode = True
    else:
        panic_mode = False

# Main loop for display and button events
try:
    while True:
        screen.fill(WHITE)  # Clear the screen

        # Draw panic/stop/resume button
        if panic_mode:
            pygame.draw.rect(screen, GREEN, panic_button)
            button_text = "Resume"
        else:
            pygame.draw.rect(screen, RED, panic_button)
            button_text = "Panic Stop"
        screen.blit(pygame.font.SysFont(None, 25).render(button_text, True, BLACK), (
