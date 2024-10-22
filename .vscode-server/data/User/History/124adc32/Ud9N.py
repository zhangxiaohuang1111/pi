
import pygame
import os
import sys
import RPi.GPIO as GPIO
from time import sleep
from threading import Timer

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()

# Screen setup
screen_width, screen_height = 320, 240
lcd = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Quit Button')

# Font setup
font_big = pygame.font.Font(None, 50)

# Button position and size
quit_button_rect = pygame.Rect(screen_width // 2 - 60, screen_height - 60, 120, 50)  # Center at the bottom

# GPIO setup for bailout button (adjust according to your GPIO pin)
BAILOUT_BUTTON_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(BAILOUT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Quit application on bailout button press
def bailout_button_pressed(channel):
    print("Bailout button pressed!")
    cleanup_and_exit()

# Bind GPIO event detection
GPIO.add_event_detect(BAILOUT_BUTTON_PIN, GPIO.FALLING, callback=bailout_button_pressed, bouncetime=300)

# Timeout handler
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

# Set the timeout duration (e.g., 30 seconds)
timeout_duration = 30
timer = Timer(timeout_duration, on_timeout)
timer.start()

# Function to draw the quit button
def draw_quit_button():
    lcd.fill(BLACK)  # Clear screen
    pygame.draw.rect(lcd, WHITE, quit_button_rect, 2)  # Draw quit button border
    quit_text = font_big.render('Quit', True, WHITE)
    lcd.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 10))
    pygame.display.update()

# Handle cleanup and quitting
def cleanup_and_exit():
    GPIO.cleanup()  # Clean up GPIO
    pygame.quit()
    sys.exit()

# Main loop
def main():
    draw_quit_button()

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cleanup_and_exit()

                # Check for mouse click on the quit button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button_rect.collidepoint(event.pos):
                        print("Quit button pressed!")
                        cleanup_and_exit()

            sleep(0.1)

    except KeyboardInterrupt:
        pass

    finally:
        cleanup_and_exit()

if __name__ == "__main__":
    main()