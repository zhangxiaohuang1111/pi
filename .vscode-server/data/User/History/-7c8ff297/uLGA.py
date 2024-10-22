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
speed1 = [6, 10]  # Speed for ball1
speed2 = [4, 5]  # Speed for ball2
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
        
        # Swap the normal velocity components (assuming equal mass)
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

# Handle ball movement, edge detection, and collision
def handle_ball_movement():
    global ballrect1, ballrect2, speed1, speed2
    
    # Perform edge detection for both balls
    edge_detection(ballrect1, speed1, 320, 240)
    edge_detection(ballrect2, speed2, 320, 240)

    # Move the balls
    ballrect1 = ballrect1.move(speed1)
    ballrect2 = ballrect2.move(speed2)

    # Handle collision between the two balls
    handle_collision(ballrect1, ballrect2, speed1, speed2, ballrect1.width // 2, ballrect2.width // 2)

    # Fill the screen with black
    lcd.fill(BLACK)

    # Draw the balls at their new positions
    lcd.blit(ball1, ballrect1)
    lcd.blit(ball2, ballrect2)

    # Redraw the buttons on top of the animation
    draw_level2_buttons()

    pygame.display.flip()
# Poll the button state in the main loop
def check_quit_button():
    if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:  # Detect if button is pressed
        print("Bail out button pressed! Exiting...")
        pygame.quit()
        GPIO.cleanup()
        exit()

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

    # Check if the quit button is pressed
    check_quit_button()  # Poll the quit button state

    # Perform edge detection and update speed accordingly
    edge_detection(ballrect1, speed1, width, height)
    edge_detection(ballrect2, speed2, width, height)

    # Move ball1 by its speed vector
    ballrect1 = ballrect1.move(speed1)

    # Move ball2 by its speed vector
    ballrect2 = ballrect2.move(speed2)

    # Handle collision between the two balls
    handle_collision(ballrect1, ballrect2, speed1, speed2, ballrect1.width // 2, ballrect2.width // 2)

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