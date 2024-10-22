import pygame
import os
import time
import RPi.GPIO as GPIO  # Import GPIO library for button control
import math
import random

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

# Load ball image
ball_image = pygame.image.load("goldenball.png")

# Function for creating ball data (image, rect, speed)
def create_ball(image, size, screen_width, screen_height):
    ball = pygame.transform.scale(image, size)  # Resize ball
    ball_rect = ball.get_rect()  # Get ball rect
    ball_rect.topleft = (random.randint(0, screen_width - size[0]), random.randint(0, screen_height - size[1]))  # Set random position
    speed = [random.randint(1, 3), random.randint(1, 3)]  # Set random speed
    return ball, ball_rect, speed

# Create 7 balls with random sizes and speeds
balls = []
for i in range(7):
    size = (random.randint(20, 50), random.randint(20, 50))  # Random size between 20x20 and 50x50
    balls.append(create_ball(ball_image, size, width, height))

# Function to handle collision between two balls using improved physics
def handle_collision(ballrect1, ballrect2, speed1, speed2, radius1, radius2):
    dx = ballrect1.centerx - ballrect2.centerx
    dy = ballrect1.centery - ballrect2.centery
    distance = math.hypot(dx, dy)

    if distance < (radius1 + radius2):  # If balls are touching or overlapping
        print("Collision detected!")
        
        # Calculate the normal and tangent unit vectors
        nx = dx / distance
        ny = dy / distance
        
        # Tangent vector is perpendicular to the normal vector
        tx = -ny
        ty = nx
        
        # Project the velocities onto the normal and tangent vectors
        v1n = speed1[0] * nx + speed1[1] * ny  # Velocity along the normal for ball1
        v1t = speed1[0] * tx + speed1[1] * ty  # Velocity along the tangent for ball1
        v2n = speed2[0] * nx + speed2[1] * ny  # Velocity along the normal for ball2
        v2t = speed2[0] * tx + speed2[1] * ty  # Velocity along the tangent for ball2
        
        # After collision, the tangent components remain unchanged
        # But the normal components are swapped (assuming equal mass)
        v1n, v2n = v2n, v1n
        
        # Reconstruct the velocity vectors from the normal and tangent components
        speed1[0] = v1n * nx + v1t * tx
        speed1[1] = v1n * ny + v1t * ty
        speed2[0] = v2n * nx + v2t * tx
        speed2[1] = v2n * ny + v2t * ty

        # Adjust the positions to ensure balls don't overlap after the collision
        overlap = (radius1 + radius2) - distance
        ballrect1.x += overlap * nx / 2
        ballrect1.y += overlap * ny / 2
        ballrect2.x -= overlap * nx / 2
        ballrect2.y -= overlap * ny / 2

# Function for edge detection and handling bounce
def edge_detection(ballrect, speed, screen_width, screen_height):
    """Detects if the ball hits the screen edges and reverses its speed."""
    if ballrect.left < 0 or ballrect.right > screen_width:
        speed[0] = -speed[0]  # Reverse horizontal direction
    if ballrect.top < 0 or ballrect.bottom > screen_height:
        speed[1] = -speed[1]  # Reverse vertical direction

# Set a timeout (e.g., 30 seconds)
timeout = 400  # Timeout after 30 seconds
start_time = time.time()  # Record the start time

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            GPIO.cleanup()
            exit()

    # Clear the screen before drawing
    screen.fill(black)

    # Update each ball's position, edge detection, and check for collisions
    for i in range(len(balls)):
        ball1, ballrect1, speed1 = balls[i]
        
        # Edge detection
        edge_detection(ballrect1, speed1, width, height)

        # Update ball position
        ballrect1 = ballrect1.move(speed1)

        # Check collision with other balls
        for j in range(i + 1, len(balls)):
            ball2, ballrect2, speed2 = balls[j]
            handle_collision(ballrect1, ballrect2, speed1, speed2, ballrect1.width // 2, ballrect2.width // 2)

        # Draw the ball on the screen
        screen.blit(ball1, ballrect1)

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