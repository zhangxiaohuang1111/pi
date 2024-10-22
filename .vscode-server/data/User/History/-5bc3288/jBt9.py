import pygame
import os
import time
import RPi.GPIO as GPIO
import math

# Set environment variables for piTFT
os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Use framebuffer console driver
os.putenv('SDL_FBDEV', '/dev/fb1')  # Set framebuffer device

pygame.init()

# Set up GPIO for bail out button
BAILOUT_BUTTON_PIN = 17  # Assume GPIO17 is used for the bail out button

GPIO.setmode(GPIO.BCM)
GPIO.setup(BAILOUT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def bailout_callback(channel):
    print("Bail out button pressed! Exiting...")
    pygame.quit()
    GPIO.cleanup()
    exit()

# Add event detect for bailout button
GPIO.add_event_detect(BAILOUT_BUTTON_PIN, GPIO.FALLING, callback=bailout_callback, bouncetime=300)

# Screen setup
size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)

# Load two ball images
ball1 = pygame.image.load("goldenball.png")
ball2 = pygame.image.load("goldenball.png")

# Scale ball1 and ball2 to different sizes
ball1 = pygame.transform.scale(ball1, (50, 50))  # Ball 1 is 50x50 pixels
ball2 = pygame.transform.scale(ball2, (30, 30))  # Ball 2 is 30x30 pixels

# Get the rectangular areas of the two balls
ballrect1 = ball1.get_rect()
ballrect2 = ball2.get_rect()

# Set initial positions for the balls (ensure they are within the screen bounds)
ballrect1.x, ballrect1.y = 50, 50  # Ball 1 initial position
ballrect2.x, ballrect2.y = 200, 100  # Ball 2 initial position (ensure not at bottom)

# Set the speed for each ball (increase speeds)
speed1 = [4, 4]  # Increased speed for ball1
speed2 = [6, 2]  # Increased speed for ball2

# Masses proportional to size (bigger ball = bigger mass)
mass1 = 50  # mass of ball1
mass2 = 30  # mass of ball2

# Set a timeout (e.g., 30 seconds)
timeout = 30  # Timeout after 30 seconds
start_time = time.time()  # Record the start time

def handle_collision(rect1, rect2, speed1, speed2, mass1, mass2):
    """Handles elastic collision between two balls and prevents overlap."""
    dx = rect1.centerx - rect2.centerx
    dy = rect1.centery - rect2.centery
    distance = math.hypot(dx, dy)  # Calculate distance between centers

    # If balls are touching or overlapping (distance < sum of radii)
    if distance < (rect1.width / 2 + rect2.width / 2):
        # Normal vector (direction of the collision)
        nx, ny = dx / distance, dy / distance

        # Relative velocity along the normal
        dvx = speed1[0] - speed2[0]
        dvy = speed1[1] - speed2[1]
        rel_vel = dvx * nx + dvy * ny

        # If the balls are moving towards each other
        if rel_vel > 0:
            # Calculate the impulse along the normal direction
            impulse = 2 * rel_vel / (mass1 + mass2)

            # Update velocities using the impulse
            speed1[0] -= impulse * mass2 * nx
            speed1[1] -= impulse * mass2 * ny
            speed2[0] += impulse * mass1 * nx
            speed2[1] += impulse * mass1 * ny

            # Resolve overlap: Move the balls apart based on their masses
            overlap = (rect1.width / 2 + rect2.width / 2) - distance
            rect1.x += overlap * (mass2 / (mass1 + mass2)) * nx
            rect1.y += overlap * (mass2 / (mass1 + mass2)) * ny
            rect2.x -= overlap * (mass1 / (mass1 + mass2)) * nx
            rect2.y -= overlap * (mass1 / (mass1 + mass2)) * ny

while True:
    # Move ball1 by its speed vector
    ballrect1 = ballrect1.move(speed1)
    if ballrect1.left < 0 or ballrect1.right > width:
        speed1[0] = -speed1[0]
    if ballrect1.top < 0 or ballrect1.bottom > height:
        speed1[1] = -speed1[1]  # Ensure it bounces off bottom and top
        print(f"Ball 1 speed: {speed1}")

    # Move ball2 by its speed vector
    ballrect2 = ballrect2.move(speed2)
    if ballrect2.left < 0 or ballrect2.right > width:
        speed2[0] = -speed2[0]
    if ballrect2.top < 0 or ballrect2.bottom > height:
        speed2[1] = -speed2[1]  # Ensure it bounces off bottom and top
        print(f"Ball 2 speed: {speed2}")

    # Check for collisions between the two balls
    handle_collision(ballrect1, ballrect2, speed1, speed2, mass1, mass2)

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