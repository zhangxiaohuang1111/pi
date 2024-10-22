import pygame
import pigame
import sys
import os
import RPi.GPIO as GPIO
from time import sleep
from threading import Timer
from pygame.locals import *

# Colours
WHITE = (255, 255, 255)

# Set environment variables
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')

# Initialize pygame and pigame for PiTFT
pygame.init()
pitft = pigame.PiTft()  # Initialize PiTFT

# Set up GPIO for the physical 'bail out' button
BAILOUT_BUTTON_PIN = 17  # PiTFT button on GPIO 17
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
lcd.fill((0, 0, 0))
pygame.display.update()

font_big = pygame.font.Font(None, 50)

# Only one button: Quit
touch_buttons = {'Quit': (160, 200)}  # Quit button at the bottom center

# Draw the quit button
def draw_buttons():
    lcd.fill((0, 0, 0))  # Clear the screen with black
    for k, v in touch_buttons.items():
        text_surface = font_big.render('%s' % k, True, WHITE)
        rect = text_surface.get_rect(center=v)
        pygame.draw.rect(lcd, WHITE, rect, 2)  # Draw button border
        lcd.blit(text_surface, rect)
    pygame.display.update()

# Cleanup function for safe exit
def cleanup_and_exit():
    print("Exiting...")
    pygame.quit()  # Quit pygame
    GPIO.cleanup()  # Clean up GPIO pins
    sys.exit()  # Exit the program
    del(pitft)

# Timeout function to quit the program after a set duration
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

# Set the timer for auto-exit after 30 seconds
timeout_duration = 30  # 30 seconds timeout duration
timer = Timer(timeout_duration, on_timeout)
timer.start()

# Function to reset the timer when user interacts with the screen
def reset_timer():
    global timer
    timer.cancel()  # Cancel the current timer
    timer = Timer(timeout_duration, on_timeout)  # Create a new timer
    timer.start()  # Start the new timer

# Main loop
try:
    draw_buttons()

    while True:
        pitft.update()  # Update PiTFT touch events

        # Scan touchscreen events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:  # Only handle the button down event
                x, y = pygame.mouse.get_pos()
                print(f"Touch detected at: ({x}, {y})")

                # If touch is within the "Quit" button
                if y > 120 and 80 < x < 240:  # Lower half of the screen
                    print("Quit button pressed!")
                    cleanup_and_exit()  # Properly exit the program

                reset_timer()  # Reset the timeout whenever the screen is touched

        # Handle GPIO bailout button (PiTFT GPIO 17)
        if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
            print("Bailout button detected!")
            cleanup_and_exit()

        sleep(0.1)  # Small delay to avoid excessive CPU usage

except KeyboardInterrupt:
    cleanup_and_exit()