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
speed = [2, 2]  # Set the ball's movement speed in both x and y directions
black = 0, 0, 0  # RGB value for black color

screen = pygame.display.set_mode(size)  # Create a screen with the specified size
ball = pygame.image.load("goldenball.png")  # Load the ball image
ballrect = ball.get_rect()  # Get the rectangular area of the ball

# Set a timeout (e.g., 30 seconds)
timeout = 30  # Timeout after 30 seconds
start_time = time.time()  # Record the start time

while True:
    ballrect = ballrect.move(speed)  # Move the ball by the speed vector
    if ballrect.left < 0 or ballrect.right > width:  # If the ball hits the left or right screen edge
        speed[0] = -speed[0]  # Reverse the horizontal direction
    if ballrect.top < 0 or ballrect.bottom > height:  # If the ball hits the top or bottom screen edge
        speed[1] = -speed[1]  # Reverse the vertical direction

    screen.fill(black)  # Erase the work space (fill it with black)
    screen.blit(ball, ballrect)  # Draw the ball on the screen at the new position
    pygame.display.flip()  # Update the display with the new ball position

    # Check if timeout has been reached
    if time.time() - start_time > timeout:
        print("Timeout reached, exiting...")
        break

    time.sleep(0.01)  # Reduce CPU usage

# Cleanup before exiting
pygame.quit()
GPIO.cleanup()