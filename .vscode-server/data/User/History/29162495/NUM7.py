import pygame
import os
import sys
import RPi.GPIO as GPIO
from time import sleep, time
from threading import Timer
from pygame.locals import *

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set environment variables for PiTFT
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')

# Initialize pygame for PiTFT
pygame.init()

# GPIO for physical bail-out button (GPIO 17)
BAILOUT_BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BAILOUT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to handle GPIO bailout button press
def bailout_button_pressed(channel):
    print("Bailout button pressed!")
    cleanup_and_exit()

# Bind GPIO event detection for the bailout button
GPIO.add_event_detect(BAILOUT_BUTTON_PIN, GPIO.FALLING, callback=bailout_button_pressed, bouncetime=300)

# Set up the screen
lcd = pygame.display.set_mode((320, 240))
lcd.fill(BLACK)
pygame.display.update()

font_big = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Define buttons
start_button_rect = pygame.Rect(20, 240 - 50, 120, 40)  # Start button on the left
quit_button_rect = pygame.Rect(320 - 140, 240 - 50, 120, 40)  # Quit button on the right

# Draw buttons
def draw_buttons():
    # Start button
    pygame.draw.rect(lcd, WHITE, start_button_rect, 2)
    start_text = font_big.render('Start', True, WHITE)
    lcd.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 5))

    # Quit button
    pygame.draw.rect(lcd, WHITE, quit_button_rect, 2)
    quit_text = font_big.render('Quit', True, WHITE)
    lcd.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 5))

    pygame.display.update()

# Function to run the two_collide.py animation (integrating the code)
def start_two_collide():
    print("Starting two_collide.py animation...")
    
    # Variables for the two balls
    ball1 = pygame.image.load("goldenball.png")
    ball2 = pygame.image.load("goldenball.png")

    # Scale the balls
    ball1 = pygame.transform.scale(ball1, (50, 50))
    ball2 = pygame.transform.scale(ball2, (30, 30))

    # Get the ball rects
    ballrect1 = ball1.get_rect(topleft=(50, 50))
    ballrect2 = ball2.get_rect(topleft=(200, 150))

    speed1 = [6, 10]
    speed2 = [4, 5]

    start_time = time()  # Record start time for timeout
    timeout = 30  # 30 seconds timeout

    running_animation = True
    while running_animation:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Continue handling buttons during animation
                if quit_button_rect.collidepoint(x, y):
                    print("Quit button pressed!")
                    cleanup_and_exit()

                print(f"Touch at: ({x}, {y})")  # Display coordinates

        # Edge detection and bounce logic
        if ballrect1.left < 0 or ballrect1.right > 320:
            speed1[0] = -speed1[0]
        if ballrect1.top < 0 or ballrect1.bottom > 240:
            speed1[1] = -speed1[1]
        
        if ballrect2.left < 0 or ballrect2.right > 320:
            speed2[0] = -speed2[0]
        if ballrect2.top < 0 or ballrect2.bottom > 240:
            speed2[1] = -speed2[1]

        # Move the balls
        ballrect1 = ballrect1.move(speed1)
        ballrect2 = ballrect2.move(speed2)

        # Fill screen
        lcd.fill(BLACK)
        lcd.blit(ball1, ballrect1)
        lcd.blit(ball2, ballrect2)

        # Redraw buttons
        draw_buttons()

        pygame.display.flip()

        # Timeout condition
        if time() - start_time > timeout:
            print("Timeout reached, exiting...")
            cleanup_and_exit()

        sleep(0.01)  # Reduce CPU usage

# Function to display touch coordinates on the screen
def display_touch(x, y):
    lcd.fill(BLACK)
    draw_buttons()
    touch_text = font_small.render(f'Touch at ({x}, {y})', True, WHITE)
    lcd.blit(touch_text, (80, 100))
    pygame.display.update()
    print(f"Touch at: ({x}, {y})")

# Cleanup function
def cleanup_and_exit():
    global running
    print("Exiting...")
    timer.cancel()
    running = False
    pygame.quit()
    GPIO.cleanup()
    os._exit(0)

# Timeout function
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

# Set the timer for auto-exit after 30 seconds
timeout_duration = 30
timer = Timer(timeout_duration, on_timeout)
timer.start()

# Reset the timer on interaction
def reset_timer():
    global timer
    timer.cancel()
    timer = Timer(timeout_duration, on_timeout)
    timer.start()

# Main loop
try:
    draw_buttons()

    running = True
    while running:
        pitft.update()  # Update PiTFT touch events

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                display_touch(x, y)

                # If Start button pressed
                if start_button_rect.collidepoint(x, y):
                    print("Start button pressed!")
                    start_two_collide()  # Start animation

                # If Quit button pressed
                elif quit_button_rect.collidepoint(x, y):
                    print("Quit button pressed!")
                    cleanup_and_exit()

                reset_timer()  # Reset the timeout

        # Handle GPIO bailout button
        if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
            print("Bailout button detected!")
            cleanup_and_exit()

        sleep(0.1)

except KeyboardInterrupt:
    cleanup_and_exit()