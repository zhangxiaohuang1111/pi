import pygame
import os
import time
import RPi.GPIO as GPIO  # Import GPIO library for button control

# Set environment variables for piTFT
os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use framebuffer console driver
os.putenv('SDL_FBDEV', '/dev/fb0')  # Set framebuffer device

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
ball2 = pygame.image.load("goldenball.png")

# Scale ball1 and ball2 to different sizes
ball1 = pygame.transform.scale(ball1, (50, 50))  # Make ball1 50x50 pixels
ball2 = pygame.transform.scale(ball2, (30, 30))  # Make ball2 30x30 pixels

# Get the rectangular areas of the two balls
ballrect1 = ball1.get_rect()
ballrect2 = ball2.get_rect()

# Set initial positions of the balls
ballrect1.topleft = (50, 50)
ballrect2.topleft = (200, 150)

# Set the speed for each ball (ball1 and ball2 have different speeds)
speed1 = [2, 2]  # Speed for ball1
speed2 = [3, 1]  # Speed for ball2

# Function to handle collision between two balls and adjust their positions
def handle_collision(ballrect1, ballrect2, speed1, speed2):
    if ballrect1.colliderect(ballrect2):
        # Swap speeds on collision to simulate a bounce
        speed1[0], speed2[0] = speed2[0], speed1[0]
        speed1[1], speed2[1] = speed2[1], speed1[1]

        # Adjust positions so that the balls no longer overlap
        overlap_x = min(ballrect1.right - ballrect2.left, ballrect2.right - ballrect1.left)
        overlap_y = min(ballrect1.bottom - ballrect2.top, ballrect2.bottom - ballrect1.top)

        # Move ball1 and ball2 slightly apart in the x direction if overlap is larger in x
        if overlap_x > overlap_y:
            if ballrect1.centerx < ballrect2.centerx:
                ballrect1.right -= overlap_x // 2
                ballrect2.left += overlap_x // 2
            else:
                ballrect1.left += overlap_x // 2
                ballrect2.right -= overlap_x // 2
        # Move ball1 and ball2 slightly apart in the y direction if overlap is larger in y
        else:
            if ballrect1.centery < ballrect2.centery:
                ballrect1.bottom -= overlap_y // 2
                ballrect2.top += overlap_y // 2
            else:
                ballrect1.top += overlap_y // 2
                ballrect2.bottom -= overlap_y // 2

# Set a timeout (e.g., 30 seconds)
timeout = 400  # Timeout after 30 seconds
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

    # Handle collision between the two balls
    handle_collision(ballrect1, ballrect2, speed1, speed2)

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