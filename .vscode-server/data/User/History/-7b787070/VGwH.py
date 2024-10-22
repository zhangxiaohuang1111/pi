import pygame
import os
import time
import RPi.GPIO as GPIO  # Import GPIO library for button control

# Set environment variables for piTFT
os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use framebuffer console driver
os.putenv('SDL_FBDEV', '/dev/fb1')  # Set framebuffer device

pygame.init()

# Set up GPIO for bail out button
BAILOUT_BUTTON_PIN = 17  # Assume GPIO17 is used for the bail out button

GPIO.setmode(GPIO.BCM)
GPIO.setup(BAILOUT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to handle button press event
def bailout_callback(channel):
    print("Bail out button pressed! Exiting...")
    pygame.quit()
    GPIO.cleanup()
    exit()

# Add event detect for bailout button
GPIO.add_event_detect(BAILOUT_BUTTON_PIN, GPIO.FALLING, callback=bailout_callback, bouncetime=300)

# Screen setup
size = width, height = 320, 240  # Set the screen size to 320x240
black = 0, 0, 0  # RGB value for black color

screen = pygame.display.set_mode(size)  # Create a screen with the specified size

# Load two ball images
ball1 = pygame.image.load("goldenball.png")
ball2 = pygame.image.load("blueball.png")

# Get the rectangular areas of the two balls
ballrect1 = ball1.get_rect()
ballrect2 = ball2.get_rect()

# Set the speed for each ball (ball1 and ball2 have different speeds)
speed1 = [2, 2]  # Speed for ball1
speed2 = [3, 1]  # Speed for ball2

# Set a timeout (e.g., 30 seconds)
timeout = 30  # Timeout after 30 seconds
start_time = time.time()  # Record the start time

while True:
    # Move ball1 by its speed vector
    ballrect1 = ballrect1.move(speed1)
    if ballrect1.left < 0 or ballrect1.right > width:
        speed1[0] = -speed1[0]  # Reverse horizontal direction for ball1
    if ballrect1.top < 0 or ballrect1.bottom > height:
        speed1[1] = -speed1[1]  # Reverse vertical direction for ball1

    # Move ball2 by its speed vector
    ballrect2 = ballrect2.move(speed2)
    if ballrect2.left < 0 or ballrect2.right > width:
        speed2[0] = -speed2[0]  # Reverse horizontal direction for ball2
    if ballrect2.top < 0 or ballrect2.bottom > height:
        speed2[1] = -speed2[1]  # Reverse vertical direction for ball2

    # Fill the screen with black to erase the previous positions of the balls
    screen.fill(black)

    # Draw both balls at their new positions
    screen.blit(ball1, ballrect1)
    screen.blit(ball2, ballrect2)

    # Update the display with the new positions of the balls
    pygame.display.flip()

    # Check if timeout has been reached
    if time.time() - start_time > timeout:
        print("Timeout reached, exiting...")
        break

    time.sleep(0.01)  # Reduce CPU usage

# Cleanup before exiting
pygame.quit()
GPIO.cleanup()