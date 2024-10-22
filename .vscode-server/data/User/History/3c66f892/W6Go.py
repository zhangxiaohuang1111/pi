import pygame
import sys
import RPi.GPIO as GPIO
import os
from time import sleep
from threading import Timer
from pygame.locals import *

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')
os.putenv('DISPLAY','')

# Screen resolution
SCREEN_WIDTH, SCREEN_HEIGHT = 320, 240

# Button configuration
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 40
START_BUTTON_POS = (20, SCREEN_HEIGHT - 50)
QUIT_BUTTON_POS = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 50)

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

# Initialize pygame
pygame.init()
lcd = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
lcd.fill(BLACK)
pygame.display.update()

# Font setup
font_big = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Timeout settings
TIMEOUT_DURATION = 5  # in seconds
timer = None

# Draw buttons once to avoid redrawing unnecessarily
def draw_buttons():
    pygame.draw.rect(lcd, WHITE, (*START_BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
    pygame.draw.rect(lcd, WHITE, (*QUIT_BUTTON_POS, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
    start_text = font_small.render('Start', True, WHITE)
    quit_text = font_small.render('Quit', True, WHITE)
    lcd.blit(start_text, (START_BUTTON_POS[0] + 10, START_BUTTON_POS[1] + 5))
    lcd.blit(quit_text, (QUIT_BUTTON_POS[0] + 10, QUIT_BUTTON_POS[1] + 5))
    pygame.display.update()

# Cleanup function for safe exit
def cleanup_and_exit():
    # Cancel the timer before exiting
    if timer is not None:
        timer.cancel()
    
    # Clean up GPIO pins
    GPIO.cleanup()
    
    # Quit pygame and exit Python
    pygame.quit()
    sys.exit()

# Timeout function to quit the program after 30 seconds
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

# Reset or start the timeout timer
def reset_timer():
    global timer
    if timer:
        timer.cancel()  # Cancel the current timer
    timer = Timer(TIMEOUT_DURATION, on_timeout)  # Create a new timer
    timer.start()  # Start the new timer

# Main loop
def main():
    global timer
    reset_timer()
    draw_buttons()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    cleanup_and_exit()

                # Capture touch or mouse event
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    print(f"Touch at: ({x}, {y})")

                    # Clear screen except buttons
                    lcd.fill(BLACK)
                    draw_buttons()

                    # Display coordinates on screen
                    touch_text = font_small.render(f'Touch at ({x}, {y})', True, WHITE)
                    lcd.blit(touch_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 20))
                    pygame.display.update()

                    # Check if the "Quit" button is pressed
                    if QUIT_BUTTON_POS[0] <= x <= QUIT_BUTTON_POS[0] + BUTTON_WIDTH and QUIT_BUTTON_POS[1] <= y <= QUIT_BUTTON_POS[1] + BUTTON_HEIGHT:
                        print("Quit button pressed!")
                        cleanup_and_exit()

                    # Reset the timeout timer on touch
                    reset_timer()

            # Handle GPIO bailout button (PiTFT GPIO 17)
            if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
                print("Bailout button detected!")
                cleanup_and_exit()

            sleep(0.05)  # Small delay to reduce CPU usage

    except KeyboardInterrupt:
        cleanup_and_exit()

if __name__ == "__main__":
    main()