import pygame  # Import pygame graphics library
import os  # For OS calls

os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')

pygame.init()

size = width, height = 320, 240  # Set the screen size to 320x240
speed = [2, 2]  # Set the ball's movement speed in both x and y directions
black = 0, 0, 0  # RGB value for black color

screen = pygame.display.set_mode(size)  # Create a screen with the specified size
ball = pygame.image.load("goldenball.png")  # Load the ball image
ballrect = ball.get_rect()  # Get the rectangular area of the ball

while 1:
    ballrect = ballrect.move(speed)  # Move the ball by the speed vector
    if ballrect.left < 0 or ballrect.right > width:  # If the ball hits the left or right screen edge
        speed[0] = -speed[0]  # Reverse the horizontal direction
    if ballrect.top < 0 or ballrect.bottom > height:  # If the ball hits the top or bottom screen edge
        speed[1] = -speed[1]  # Reverse the vertical direction

    screen.fill(black)  # Erase the work space (fill it with black)
    screen.blit(ball, ballrect)  # Draw the ball on the screen at the new position
    pygame.display.flip()  # Update the display with the new ball position