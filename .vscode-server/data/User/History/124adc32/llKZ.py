import pygame
import os
import sys
import RPi.GPIO as GPIO
from time import sleep
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

        # Add a small delay to avoid excessive CPU usage
        sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    cleanup_and_exit()