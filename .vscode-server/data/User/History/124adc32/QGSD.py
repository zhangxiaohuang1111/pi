import pygame
import os
import sys
import RPi.GPIO as GPIO
from time import sleep, time
from threading import Timer
from pygame.locals import *

# Colours
WHITE = (255, 255, 255)

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

# Set up screen
lcd = pygame.display.set_mode((320, 240))
lcd.fill((0, 0, 0))
pygame.display.update()

# Font setup
font_big = pygame.font.Font(None, 50)

# Touch buttons with positions
touch_buttons = {'Shutdown': (80, 60), 'Quit': (240, 60), '17 off': (80, 180), '4 off': (240, 180)}

# Draw buttons on the screen
for k, v in touch_buttons.items():
    text_surface = font_big.render('%s' % k, True, WHITE)
    rect = text_surface.get_rect(center=v)
    lcd.blit(text_surface, rect)

pygame.display.update()

# Timeout function to quit the program after 30 seconds
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

# Start a timer for auto-exit after 30 seconds
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
    while True:
        # Scan touchscreen events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(x, y)

            elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                print(x, y)
                
                # Check which part of the screen was touched
                if y > 120:  # Lower half of the screen
                    if x < 160:
                        print("17off")
                        # Here you can add actions for '17 off'
                    else:
                        print("4off")
                        # Here you can add actions for '4 off'
                else:  # Upper half of the screen
                    if x < 160:
                        print("Shutdown selected")
                        pygame.quit()
                        os.system("sudo poweroff")  # Shutdown the Raspberry Pi
                        sys.exit(0)
                    else:
                        print("Quit selected")
                        cleanup_and_exit()

                reset_timer()  # Reset the timeout whenever the screen is touched

        # Handle GPIO bailout button (PiTFT GPIO 17)
        if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
            print("Bailout button detected!")
            cleanup_and_exit()

        sleep(0.1)  # Small delay for smoother event handling

except KeyboardInterrupt:
    pass

finally:
    cleanup_and_exit()