import RPi.GPIO as GPIO
import time
import pygame
import os
import threading
import signal
import sys
import pigame
from pygame.locals import *

# GPIO Pin Setup for Motor A and Motor B
AIN1 = 5  # Motor A Direction Pin 1
AIN2 = 6  # Motor A Direction Pin 2
BIN1 = 20 # Motor B Direction Pin 1
BIN2 = 21 # Motor B Direction Pin 2
PWMA = 16 # Motor A PWM Control (also used for Motor B)

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set environment variables for PiTFT
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')

# Initialize pygame for PiTFT
pygame.init()
pitft = pigame.PiTft()  # Initialize PiTFT
screen = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible(True)
font_small = pygame.font.Font(None, 17)

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

# State variables to track motor direction and timing
stateA = 0  # 0 = stopped, 1 = clockwise, 2 = counterclockwise
stateB = 0  # 0 = stopped, 1 = clockwise, 2 = counterclockwise
start_time = time.time()  # Start time for timestamp calculations

# Historical records
left_history = []
right_history = []

# Flag for display thread
running = True

# Panic stop flag and previous state variables
is_panic_stop = False
prev_stateA = 0
prev_stateB = 0

# Motor control functions
def motor_a_forward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    record_history(left_history, "Clkwise")

def motor_a_backward():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)
    record_history(left_history, "Counter-Clk")

def motor_a_stop():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    record_history(left_history, "Stop")

def motor_b_forward():
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)
    record_history(right_history, "Clkwise")

def motor_b_backward():
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)
    record_history(right_history, "Counter-Clk")

def motor_b_stop():
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    record_history(right_history, "Stop")

# Helper function to record history
def record_history(history_list, state):
    elapsed_time = int(time.time() - start_time)
    history_list.insert(0, (state, elapsed_time))
    if len(history_list) > 3:
        history_list.pop()

# Cleanup and exit function
def cleanup_and_exit():
    global running

    if not running:  # Prevent duplicate cleanup
        return

    running = False  # Stop the display thread loop

    # Wait for the display thread to finish, if not the current thread
    if threading.current_thread() != display_thread:
        if display_thread.is_alive():
            display_thread.join(timeout=1)

    # Stop PWM and cleanup GPIO safely
    try:
        pwm_a.stop()
        GPIO.cleanup()
    except Exception as e:
        print(f"Error during GPIO cleanup: {e}")

    # Quit pygame safely
    try:
        pygame.display.quit()
        pygame.quit()
    except Exception as e:
        print(f"Error during pygame quit: {e}")

    # Force exit
    print("Exiting the program.")
    os._exit(0)  # Use os._exit(0) to force quit

# Signal handler for graceful exit
def signal_handler(sig, frame):
    cleanup_and_exit()

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Panic stop and resume handler
def handle_panic_stop():
    global is_panic_stop, prev_stateA, prev_stateB, stateA, stateB
    if not is_panic_stop:
        prev_stateA = stateA
        prev_stateB = stateB
        motor_a_stop()
        motor_b_stop()
        print("Panic stop activated - Both motors stopped")
        is_panic_stop = True
    else:
        if prev_stateA == 1:
            motor_a_forward()
        elif prev_stateA == 2:
            motor_a_backward()

        if prev_stateB == 1:
            motor_b_forward()
        elif prev_stateB == 2:
            motor_b_backward()

        print("Resuming from panic stop")
        is_panic_stop = False

# Adjusted display function to include STOP/RESUME and QUIT button interactions
def update_display():
    try:
        while running:
            pitft.update()
            screen.fill(BLACK)

            # Display Left Motor history
            left_text = font_small.render("Left History", True, WHITE)
            screen.blit(left_text, (10, 10))
            for i, (state, timestamp) in enumerate(left_history[:3]):
                history_text = font_small.render(f"{state} {timestamp}s", True, WHITE)
                screen.blit(history_text, (10, 30 + i * 15))

            # Display Right Motor history
            right_text = font_small.render("Right History", True, WHITE)
            screen.blit(right_text, (170, 10))
            for i, (state, timestamp) in enumerate(right_history[:3]):
                history_text = font_small.render(f"{state} {timestamp}s", True, WHITE)
                screen.blit(history_text, (170, 30 + i * 15))

            # Draw STOP or RESUME button
            if not is_panic_stop:
                pygame.draw.circle(screen, RED, (160, 120), 30)
                stop_text = font_small.render("STOP", True, WHITE)
                screen.blit(stop_text, (145, 115))
            else:
                pygame.draw.circle(screen, GREEN, (160, 120), 30)
                resume_text = font_small.render("RESUME", True, WHITE)
                screen.blit(resume_text, (135, 115))

            # Draw QUIT button
            pygame.draw.rect(screen, WHITE, (230, 180, 80, 40), 2)  # Draw QUIT button border
            quit_text = font_small.render("QUIT", True, WHITE)
            screen.blit(quit_text, (250, 190))

            pygame.display.update()

            # Check for events to handle STOP/RESUME and QUIT button presses
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Check if STOP or RESUME button is pressed
                    if 130 <= x <= 190 and 90 <= y <= 150:  # STOP/RESUME button position and size
                        handle_panic_stop()
                    
                    # Check if QUIT button is pressed
                    elif 230 <= x <= 310 and 180 <= y <= 220:  # QUIT button position and size
                        print("QUIT button pressed")
                        cleanup_and_exit()  # Call the cleanup and exit function

            time.sleep(0.1)
    except pygame.error as e:
        print(f"Pygame error: {e}")
    finally:
        pygame.display.quit()

# Start a separate thread for the display update
display_thread = threading.Thread(target=update_display)
display_thread.start()

# Adjusted