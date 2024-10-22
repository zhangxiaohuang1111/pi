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
BLACK = (0, 0, 0)

# Set environment variables for PiTFT
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')

# Initialize pygame and pigame for PiTFT
pygame.init()
pitft = pigame.PiTft()  # Initialize PiTFT

# Set up GPIO for the physical 'bail-out' button (e.g., GPIO 17)
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
start_button_rect = pygame.Rect(60 - 60, 240 - 50, 120, 40)  # Left side for the Start button
quit_button_rect = pygame.Rect(320 - 120, 240 - 50, 120, 40)  # Right side for the Quit button

# Draw the buttons
def draw_buttons():
    # Start button
    pygame.draw.rect(lcd, WHITE, start_button_rect, 2)  # Draw button border
    start_text = font_big.render('Start', True, WHITE)
    lcd.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 5))
    
    # Quit button
    pygame.draw.rect(lcd, WHITE, quit_button_rect, 2)  # Draw button border
    quit_text = font_big.render('Quit', True, WHITE)
    lcd.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 5))
    
    pygame.display.update()

# Function to display touch coordinates on the screen and in the console
def display_touch(x, y):
    lcd.fill(BLACK)
    draw_buttons()  # Draw both buttons again after each touch
    touch_text = font_small.render(f'Touch at ({x}, {y})', True, WHITE)
    lcd.blit(touch_text, (80, 100))  # Center text in the middle of the screen
    pygame.display.update()
    print(f"Touch at: ({x}, {y})")  # Print coordinates to the console

# Cleanup function for safe exit
def cleanup_and_exit():
    global running, exiting
    if exiting:  # Prevent multiple exit attempts
        return

    print("Exiting...")
    exiting = True  # Set the flag to indicate that we are exiting
    timer.cancel()  # Cancel the timer if it's still running
    running = False  # Stop the main loop

    # Quit pygame and clean up GPIO
    try:
        pygame.quit()  # Quit pygame
        GPIO.cleanup()  # Clean up all GPIO channels
    except Exception as e:
        print(f"Error during cleanup: {e}")
    
    # Force the program to exit immediately
    os._exit(0)  # Force the program to terminate

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

# Global flags
running = True
exiting = False  # This flag prevents multiple exits

# Transition function to go from Level 1 to Level 2 menu
def level2_menu():
    print("Transition to Level 2 menu: Animation control")

# Main loop for Level 1 menu
try:
    draw_buttons()

    while running:  # Main loop runs while 'running' is True
        pitft.update()  # Update PiTFT touch events

        # Scan touchscreen events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # If touch is within the "Start" button
                if start_button_rect.collidepoint(x, y):
                    print("Start button pressed!")
                    level2_menu()  # Transition to the Level 2 menu

                # If touch is within the "Quit" button
                elif quit_button_rect.collidepoint(x, y):
                    print("Quit button pressed!")
                    cleanup_and_exit()  # Exit the program
                
                # If outside buttons, display coordinates
                else:
                    display_touch(x, y)

                reset_timer()  # Reset the timeout whenever the screen is touched

        # Handle GPIO bailout button (PiTFT GPIO 17)
        if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
            print("Bailout button detected!")
            cleanup_and_exit()

        sleep(0.1)  # Small delay to avoid excessive CPU usage

except KeyboardInterrupt:
    cleanup_and_exit()