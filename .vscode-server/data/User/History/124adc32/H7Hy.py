import pygame
import sys
import os
from pygame.locals import *

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 320, 240
lcd = pygame.display.set_mode((screen_width, screen_height))
lcd.fill(BLACK)
pygame.display.update()

# Font setup for the button text
font_big = pygame.font.Font(None, 50)

# Button position and size
quit_button_rect = pygame.Rect(screen_width // 2 - 60, screen_height - 50, 120, 40)  # Bottom of the screen

# Draw the quit button on the screen
def draw_quit_button():
    lcd.fill(BLACK)  # Clear the screen with black
    pygame.draw.rect(lcd, WHITE, quit_button_rect, 2)  # Draw button border
    quit_text = font_big.render('Quit', True, WHITE)
    lcd.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 5))
    pygame.display.update()

# Cleanup function for safe exit
def cleanup_and_exit():
    pygame.quit()
    sys.exit()

# Main loop
try:
    draw_quit_button()

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                cleanup_and_exit()

            # Touch anywhere to quit (for testing)
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(f"Touch detected at: {x}, {y}")

                # Check if the touch is within the "Quit" button
                if quit_button_rect.collidepoint(x, y):
                    print("Quit button pressed!")
                    cleanup_and_exit()

        # Add a small delay to prevent high CPU usage
        pygame.time.delay(100)

except KeyboardInterrupt:
    cleanup_and_exit()