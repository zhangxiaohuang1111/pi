import RPi.GPIO as GPIO
import time
import pygame
import os
import threading
import pigame  # Use pigame for PiTFT control
from pygame.locals import *

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motor GPIO pins
AIN1 = 5
AIN2 = 6
BIN1 = 20
BIN2 = 21
PWMA = 16

# Button GPIO pins
start_button = 17  # Start button
quit_button = 22   # Quit button

# Motor PWM setup
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)

pwm_a = GPIO.PWM(PWMA, 50)  # 50Hz PWM
pwm_a.start(0)

# PiTFT setup
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')
pygame.init()

# Initialize pigame for PiTFT interaction
pitft = pigame.PiTft()

screen = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible(False)
font_small = pygame.font.Font(None, 17)

# State variables
running = True
robot_running = False
stop_resume_state = 'STOP'

# Historical records
left_history = []
right_history = []

# Motor control functions
def motor_forward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(100)
    record_history(left_history, "Forward")
    record_history(right_history, "Forward")

def motor_backward():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(100)
    record_history(left_history, "Backward")
    record_history(right_history, "Backward")

def pivot_left():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(100)
    record_history(left_history, "Pivot L")
    record_history(right_history, "Pivot L")

def pivot_right():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(100)
    record_history(left_history, "Pivot R")
    record_history(right_history, "Pivot R")

def motor_stop():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(0)
    record_history(left_history, "Stop")
    record_history(right_history, "Stop")

# Helper function to record history
def record_history(history_list, state):
    elapsed_time = int(time.time() - start_time)
    history_list.insert(0, (state, elapsed_time))
    if len(history_list) > 3:
        history_list.pop()

# Display update function using pigame
def update_display():
    global stop_resume_state
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

            # Draw STOP/RESUME button
            if stop_resume_state == 'STOP':
                pygame.draw.circle(screen, RED, (160, 120), 30)
                stop_resume_text = font_small.render("STOP", True, WHITE)
                screen.blit(stop_resume_text, (145, 115))
            else:
                pygame.draw.circle(screen, GREEN, (160, 120), 30)
                resume_text = font_small.render("RESUME", True, WHITE)
                screen.blit(resume_text, (140, 115))

            # Draw QUIT button
            pygame.draw.rect(screen, WHITE, (230, 180, 80, 40), 2)
            quit_text = font_small.render("QUIT", True, WHITE)
            screen.blit(quit_text, (250, 190))

            pygame.display.update()

            # Handle PiTFT touchscreen events
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Handle STOP/RESUME button press
                    if 130 <= x <= 190 and 90 <= y <= 150:
                        handle_stop_resume_button()

                    # Handle QUIT button press
                    elif 230 <= x <= 310 and 180 <= y <= 220:
                        handle_quit_button()

            time.sleep(0.1)
    except pygame.error as e:
        print(f"Pygame error: {e}")
    finally:
        pygame.display.quit()

# Start the robot movement sequence
def start_run_test():
    global robot_running
    robot_running = True
    while robot_running:
        # Move forward
        motor_forward()
        time.sleep(2)
        motor_stop()
        time.sleep(1)

        # Move backward
        motor_backward()
        time.sleep(2)
        motor_stop()
        time.sleep(1)

        # Pivot left
        pivot_left()
        time.sleep(2)
        motor_stop()
        time.sleep(1)

        # Pivot right
        pivot_right()
        time.sleep(2)
        motor_stop()
        time.sleep(1)

# Handle STOP/RESUME button press
def handle_stop_resume_button():
    global stop_resume_state, robot_running
    if stop_resume_state == 'STOP':
        motor_stop()
        stop_resume_state = 'RESUME'
        robot_running = False
        print("STOP pressed - Motors stopped")
    elif stop_resume_state == 'RESUME':
        stop_resume_state = 'STOP'
        robot_running = True
        print("RESUME pressed - Resuming motors")
        start_run_test()

# Handle QUIT button press
def handle_quit_button():
    print("QUIT pressed")
    cleanup_and_exit()

# Cleanup and exit
def cleanup_and_exit():
    global running
    running = False
    motor_stop()
    pwm_a.stop()
    GPIO.cleanup()
    pygame.quit()
    os._exit(0)

# GPIO button setup and event handling
GPIO.setup(start_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(quit_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(start_button, GPIO.FALLING, callback=lambda x: start_run_test(), bouncetime=300)
GPIO.add_event_detect(quit_button, GPIO.FALLING, callback=lambda x: cleanup_and_exit(), bouncetime=300)

# Start the display update thread
display_thread = threading.Thread(target=update_display)
display_thread.start()

# Main loop
try:
    while running:
        time.sleep(0.1)
except KeyboardInterrupt:
    cleanup_and_exit()