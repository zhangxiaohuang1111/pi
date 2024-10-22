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
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

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
buttonA_stop    = 22  # Button to stop left motor
buttonB_control = 23  # Button to control right motor (clockwise/counterclockwise toggle)
buttonB_stop    = 27  # Button to stop right motor
button_exit     = 26  # Button to exit the program

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
GPIO.setup(buttonA_stop,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB_control, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB_stop,    GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_exit,     GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize PWM for both motors (shared control)
pwm_a = GPIO.PWM(PWMA, 50)  # 50Hz PWM signal
pwm_a.start(0)  # Start with motor stopped

# State variables
stateA = 0  # 0 = stopped, 1 = clockwise, 2 = counterclockwise
stateB = 0  # 0 = stopped, 1 = clockwise, 2 = counterclockwise
paused = False
prev_stateA = 0
prev_stateB = 0
stop_resume_state = 'STOP'
start_time = time.time()

# Historical records
left_history = []
right_history = []

# Flags
running = True
start_flag = False

# Motor control functions
def motor_a_forward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(100)  # Full speed
    record_history(right_history, "Clkwise")

def motor_a_backward():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(100)  # Full speed
    record_history(right_history, "Counter-Clk")

def motor_a_stop():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    record_history(right_history, "Stop")

def motor_b_forward():
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(100)  # Full speed
    record_history(left_history, "Clkwise")

def motor_b_backward():
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(100)  # Full speed
    record_history(left_history, "Counter-Clk")

def motor_b_stop():
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)
    record_history(left_history, "Stop")

def record_history(history_list, state):
    elapsed_time = int(time.time() - start_time)
    history_list.insert(0, (state, elapsed_time))
    if len(history_list) > 3:
        history_list.pop()

def cleanup_and_exit():
    # 停止所有电机
    motor_a_stop()
    motor_b_stop()

    # 停止PWM并清理GPIO
    try:
        pwm_a.stop()
        GPIO.cleanup()
        print("GPIO cleaned up.")
    except Exception as e:
        print(f"Error during GPIO cleanup: {e}")

    # 退出pygame
    pygame.quit()
    print("Exiting the program.")
    os._exit(0)

def handle_exit(channel):
    cleanup_and_exit()

GPIO.add_event_detect(button_exit, GPIO.FALLING, callback=handle_exit, bouncetime=300)

# Display function for buttons
def update_display():
    global paused, prev_stateA, prev_stateB, stop_resume_state, start_flag, running
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
                stop_resume_text = font_small.render("RESUME", True, WHITE)
                screen.blit(stop_resume_text, (140, 115))

            # Draw QUIT button
            pygame.draw.rect(screen, WHITE, (230, 180, 80, 40), 2)
            quit_text = font_small.render("QUIT", True, WHITE)
            screen.blit(quit_text, (250, 190))

            # Draw START button
            pygame.draw.rect(screen, BLUE, (10, 180, 80, 40), 2)
            start_text = font_small.render("START", True, WHITE)
            screen.blit(start_text, (30, 190))

            pygame.display.update()

            # Check for events
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # Check if START button is pressed
                    if 10 <= x <= 90 and 180 <= y <= 220:
                        start_flag = True
                        print("START button pressed - Robot starting")

                    # Check if STOP/RESUME button is pressed
                    elif 130 <= x <= 190 and 90 <= y <= 150:
                        if stop_resume_state == 'STOP':
                            paused = True
                            stop_resume_state = 'RESUME'
                            print("STOP button pressed - Robot paused")
                        elif stop_resume_state == 'RESUME':
                            paused = False
                            stop_resume_state = 'STOP'
                            print("RESUME button pressed - Robot resumed")

                    # Check if QUIT button is pressed
                    elif 230 <= x <= 310 and 180 <= y <= 220:
                        print("QUIT button pressed")
                        running = False  # 设置运行标志为False

            time.sleep(0.1)
    except pygame.error as e:
        print(f"Pygame error: {e}")
    finally:
        pygame.display.quit()

def control_robot():
    global start_flag, running, paused
    while running:
        if start_flag:
            # Movement sequence
            movements = [
                ('forward', motor_a_forward, motor_b_forward),
                ('backward', motor_a_backward, motor_b_backward),
                ('pivot_left', motor_a_forward, motor_b_backward),
                ('pivot_right', motor_a_backward, motor_b_forward)
            ]

            for move_name, motor_a_action, motor_b_action in movements:
                if not running:
                    break

                # Start movement
                motor_a_action()
                motor_b_action()

                move_time = 2  # Duration of movement in seconds
                start_move_time = time.time()

                while time.time() - start_move_time < move_time:
                    if not running:
                        break
                    if paused:
                        # If paused, stop motors and wait until unpaused
                        motor_a_stop()
                        motor_b_stop()
                        while paused and running:
                            time.sleep(0.1)
                        # After unpausing, restart the movement from the beginning
                        start_move_time = time.time()
                        motor_a_action()
                        motor_b_action()
                    time.sleep(0.1)

                # Stop motors after movement
                motor_a_stop()
                motor_b_stop()

                # Wait between movements
                wait_time = 1  # Duration to wait between movements
                start_wait_time = time.time()

                while time.time() - start_wait_time < wait_time:
                    if not running:
                        break
                    if paused:
                        while paused and running:
                            time.sleep(0.1)
                        # After unpausing, adjust the wait time
                        start_wait_time = time.time()
                    time.sleep(0.1)
        else:
            time.sleep(0.1)

# 启动用于显示更新的独立线程
display_thread = threading.Thread(target=update_display)
display_thread.start()

# 启动用于机器人控制的独立线程
control_thread = threading.Thread(target=control_robot)
control_thread.start()

# 记录程序开始的时间
program_start_time = time.time()

# 主循环，等待退出信号
try:
    while running:
        # 检查程序是否运行了超过10秒
        elapsed_time = time.time() - program_start_time
        if elapsed_time >= 300:
            print("Program has been running for 10 seconds. Exiting...")
            running = False  # 设置运行标志为False，触发退出流程
        time.sleep(0.1)
except KeyboardInterrupt:
    print("KeyboardInterrupt received")
    running = False  # 捕获Ctrl+C，设置运行标志为False

# 等待所有线程结束
display_thread.join()
control_thread.join()

# 执行清理操作并退出
cleanup_and_exit()