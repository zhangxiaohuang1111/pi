import pygame
import sys
import os
import RPi.GPIO as GPIO
from time import sleep
from threading import Timer
from pygame.locals import *

# Set environment variables before initializing pygame
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# GPIO setup for the bail-out button (PiTFT button on GPIO 17)
BAILOUT_BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BAILOUT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to handle GPIO bailout button press
def bailout_button_pressed(channel):
    print("Bailout button (GPIO 17) pressed!")
    cleanup_and_exit()

# Bind GPIO event detection for the bail-out button
GPIO.add_event_detect(BAILOUT_BUTTON_PIN, GPIO.FALLING, callback=bailout_button_pressed, bouncetime=300)

# Initialize pygame after environment variables are set
pygame.init()

# Set up the screen
screen_width, screen_height = 320, 240
lcd = pygame.display.set_mode((screen_width, screen_height))
lcd.fill(BLACK)
pygame.display.update()

# Font setup for the button text
font_big = pygame.font.Font(None, 50)

# Button position and size
quit_button_rect = pygame.Rect(screen_width // 2 - 60, screen_height - 50, 120, 40)  # Bottom of the screen

# Draw the quit button on the screen
def draw_quit_button():
    lcd.fill(BLACK)  # Clear the screen with black
    pygame.draw.rect(lcd, WHITE, quit_button_rect, 2)  # Draw button border
    quit_text = font_big.render('Quit', True, WHITE)
    lcd.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 5))
    pygame.display.update()

# Timeout function to quit the program after 30 seconds
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

# Start a timer for auto-exit after 5 seconds (for testing)
timeout_duration = 10  # Timeout duration in seconds
timer = Timer(timeout_duration, on_timeout)
timer.start()

# Function to reset the timer when user interacts with the screen
def reset_timer():
    global timer
    timer.cancel()  # Cancel the current timer
    timer = Timer(timeout_duration, on_timeout)  # Create a new timer
    timer.start()  # Start the new timer

# Cleanup function for safe exit
def cleanup_and_exit():
    GPIO.cleanup()  # Clean up GPIO pins
    pygame.quit()
    sys.exit()

# Main loop
try:
    draw_quit_button()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                cleanup_and_exit()

            # Touch anywhere to quit (for testing)
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(f"Touch detected at: {x}, {y}")

                # Check if the touch is within the "Quit" button
                if quit_button_rect.collidepoint(x, y):
                    print("Quit button pressed!")
                    cleanup_and_exit()

                reset_timer()  # Reset the timeout whenever the screen is touched

        # Handle GPIO bailout button (PiTFT GPIO 17)
        if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
            print("Bailout button detected!")
            cleanup_and_exit()

        sleep(0.1)  # Small delay to avoid excessive CPU usage

except KeyboardInterrupt:
    cleanup_and_exit()