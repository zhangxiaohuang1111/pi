import pygame
import sys
import os
import RPi.GPIO as GPIO
from time import sleep
from threading import Timer
from pygame.locals import *

# Set environment variables before initializing pygame
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')

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

# Touch button setup (multiple buttons)
touch_buttons = {
    'Shutdown': (80, 60),
    'Quit': (240, 60),
    '17 off': (80, 180),
    '4 off': (240, 180)
}

# Draw all buttons on the screen
def draw_buttons():
    lcd.fill(BLACK)  # Clear the screen
    for button, pos in touch_buttons.items():
        text_surface = font_big.render(button, True, WHITE)
        rect = text_surface.get_rect(center=pos)
        pygame.draw.rect(lcd, WHITE, rect, 2)
        lcd.blit(text_surface, rect)
    pygame.display.update()

# Timeout function to quit the program after 10 seconds of inactivity
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

# Start a timer for auto-exit after 10 seconds (for testing)
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
    draw_buttons()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                cleanup_and_exit()

            # Handle touch events
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(f"Touch detected at: ({x}, {y})")

                # Determine which button was pressed
                if y > 120:  # Bottom half of the screen
                    if x < 160:
                        print("17 off selected")
                    else:
                        print("4 off selected")
                else:  # Upper half of the screen
                    if x < 160:
                        print("Shutdown selected")
                        pygame.quit()
                        os.system("sudo poweroff")  # Shutdown the Pi
                        sys.exit(0)
                    else:
                        print("Quit selected")
                        cleanup_and_exit()

                reset_timer()  # Reset the timeout whenever the screen is touched

        # Handle GPIO bailout button (PiTFT GPIO 17)
        if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
            print("Bailout button detected!")
            cleanup_and_exit()

        sleep(0.1)  # Small delay to avoid excessive CPU usage

except KeyboardInterrupt:
    cleanup_and_exit()