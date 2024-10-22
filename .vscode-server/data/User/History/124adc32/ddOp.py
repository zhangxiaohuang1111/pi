import pygame
from pygame.locals import *
import os
from time import sleep

# Colours
WHITE = (255, 255, 255)

# Set environment variables for PiTFT
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV', '/dev/null')
os.putenv('DISPLAY', '')

# Initialize pygame
pygame.init()

# Set up the screen
lcd = pygame.display.set_mode((320, 240))
lcd.fill((0, 0, 0))
pygame.display.update()

# Font setup for the button text
font_big = pygame.font.Font(None, 50)

# Button position and size (Quit button)
quit_button_rect = pygame.Rect(160 - 60, 240 - 50, 120, 40)

# Draw the "Quit" button on the screen
def draw_quit_button():
    lcd.fill((0, 0, 0))  # Clear the screen with black
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
        # Scan touchscreen events
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                print(f"Touch detected at: ({x}, {y})")

            elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                print(f"Release detected at: ({x}, {y})")

                # Check if the touch is within the "Quit" button
                if quit_button_rect.collidepoint(x, y):
                    print("Quit button pressed!")
                    cleanup_and_exit()

        sleep(0.1)

except KeyboardInterrupt:
    cleanup_and_exit()