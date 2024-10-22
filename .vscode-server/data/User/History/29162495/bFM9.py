import pygame
import pigame
import sys
import os
import RPi.GPIO as GPIO
import math
from time import sleep
from threading import Timer
from pygame.locals import *

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set environment variables for PiTFT
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')

# Initialize pygame and pigame for PiTFT
pygame.init()
pitft = pigame.PiTft()  # Initialize PiTFT

# Set up GPIO for the physical 'bail-out' button (e.g., GPIO 17)
BAILOUT_BUTTON_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(BAILOUT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to handle GPIO bailout button press
def bailout_button_pressed(channel):
    print("Bailout button pressed!")
    cleanup_and_exit()

# Bind GPIO event detection for the bailout button
GPIO.add_event_detect(BAILOUT_BUTTON_PIN, GPIO.FALLING, callback=bailout_button_pressed, bouncetime=300)

# Set up the screen
lcd = pygame.display.set_mode((320, 240))
lcd.fill(BLACK)
pygame.display.update()

font_big = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Define buttons
start_button_rect = pygame.Rect(60 - 60, 240 - 50, 120, 40)  # Left side for the Start button
quit_button_rect = pygame.Rect(320 - 120, 240 - 50, 120, 40)  # Right side for the Quit button

# Define animation parameters (for the balls)
ball1 = pygame.image.load("goldenball.png")
ball2 = pygame.image.load("goldenball.png")

# Scale the balls to different sizes
ball1 = pygame.transform.scale(ball1, (50, 50))
ball2 = pygame.transform.scale(ball2, (30, 30))

# Get the ball rects
ballrect1 = ball1.get_rect(topleft=(50, 50))
ballrect2 = ball2.get_rect(topleft=(200, 150))

speed1 = [6, 10]
speed2 = [4, 5]

# Flag to control animation
animation_running = False

# Set up frame rate control
clock = pygame.time.Clock()  # Clock object to control frame rate

# Collision handling logic
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

# Draw the buttons
def draw_buttons():
    # Start button
    pygame.draw.rect(lcd, WHITE, start_button_rect, 2)  # Draw button border
    start_text = font_big.render('Start', True, WHITE)
    lcd.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 5))

    # Quit button
    pygame.draw.rect(lcd, WHITE, quit_button_rect, 2)  # Draw button border
    quit_text = font_big.render('Quit', True, WHITE)
    lcd.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 5))
    
    pygame.display.update()

# Function to display touch coordinates on the screen and in the console
def display_touch(x, y):
    lcd.fill(BLACK)
    draw_buttons()  # Draw both buttons again after each touch
    touch_text = font_small.render(f'Touch at ({x}, {y})', True, WHITE)
    lcd.blit(touch_text, (80, 100))  # Center text in the middle of the screen
    pygame.display.update()
    print(f"Touch at: ({x}, {y})")  # Print coordinates to the console

# Cleanup function for safe exit
def cleanup_and_exit():
    global running, exiting
    if exiting:  # Prevent multiple exit attempts
        return

    print("Exiting...")
    exiting = True  # Set the flag to indicate that we are exiting
    timer.cancel()  # Cancel the timer if it's still running
    running = False  # Stop the main loop

    # Quit pygame and clean up GPIO
    try:
        pygame.quit()  # Quit pygame
        GPIO.cleanup()  # Clean up all GPIO channels
    except Exception as e:
        print(f"Error during cleanup: {e}")
    
    # Force the program to exit immediately
    os._exit(0)  # Force the program to terminate

# Timeout function to quit the program after a set duration
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

# Set the timer for auto-exit after 30 seconds
timeout_duration = 30  # 30 seconds timeout duration
timer = Timer(timeout_duration, on_timeout)
timer.start()

# Function to reset the timer when user interacts with the screen
def reset_timer():
    global timer
    timer.cancel()  # Cancel the current timer
    timer = Timer(timeout_duration, on_timeout)  # Create a new timer
    timer.start()  # Start the new timer

# Global flags
running = True
exiting = False  # This flag prevents multiple exits

# Main loop
try:
    draw_buttons()

    while running:  # Main loop runs while 'running' is True
        pitft.update()  # Update PiTFT touch events

        # Scan touchscreen events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                display_touch(x, y)

                # If touch is within the "Start" button
                if start_button_rect.collidepoint(x, y):
                    print("Start button pressed!")
                    animation_running = True  # Start the animation

                # If touch is within the "Quit" button
                elif quit_button_rect.collidepoint(x, y):
                    print("Quit button pressed!")
                    cleanup_and_exit()  # Exit the program

                reset_timer()  # Reset the timeout whenever the screen is touched

        # Handle GPIO bailout button (PiTFT GPIO 17)
        if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
            print("Bailout button detected!")
            cleanup_and_exit()

        # If animation is running, update the ball positions
        if animation_running:
            # Edge detection and bouncing logic for ball 1
            if ballrect1.left < 0 or ballrect1.right > 320:
                speed1[0] = -speed1[0]
            if ballrect1.top < 0 or ballrect1.bottom > 240:
                speed1[1] = -speed1[1]

            # Edge detection and bouncing logic for ball 2
            if ballrect2.left < 0 or ballrect2.right > 320:
                speed2[0] = -speed2[0]
            if ballrect2.top < 0 or ballrect2.bottom > 240:
                speed2[1] = -speed2[1]

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
            draw_buttons()
            
            # Update the display
            pygame.display.flip()

        # Control frame rate (limit to 60 FPS)
        clock.tick(60)

except KeyboardInterrupt:
    cleanup_and_exit()