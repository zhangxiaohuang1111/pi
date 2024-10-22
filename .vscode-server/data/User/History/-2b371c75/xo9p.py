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

SPEED_MULTIPLIER = 1.2  # Increase or decrease speed by 20%
MIN_SPEED = 1  # Minimum speed for any ball to prevent stopping

# Define buttons for Level 1 (Start/Quit)
start_button_rect = pygame.Rect(60 - 60, 240 - 50, 120, 40)
quit_button_rect = pygame.Rect(320 - 120, 240 - 50, 120, 40)

# Define buttons for Level 2 (Pause, Faster, Slower, Back) in a single row
button_width = 70  # Narrower
button_height = 50  # Taller

pause_button_rect = pygame.Rect(10, 200, button_width, button_height)    # Pause button on the far left
faster_button_rect = pygame.Rect(90, 200, button_width, button_height)  # Faster button next to Pause
slower_button_rect = pygame.Rect(170, 200, button_width, button_height)  # Slower button next to Faster
back_button_rect = pygame.Rect(250, 200, button_width, button_height)    # Back button next to Slower

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
MAX_SPEED = 15  # Maximum speed limit
MIN_SPEED = 1   # Minimum speed limit

# Flag to control animation
animation_running = False
animation_paused = False

# Global flags for controlling the main loop and exit
running = True
exiting = False

# Timeout duration and timer setup
timeout_duration = 30  # 30 seconds timeout duration
timer = None  # Initialize timer variable

# Set up frame rate control
clock = pygame.time.Clock()

# Timeout function to quit the program after a set duration
def on_timeout():
    print("Timeout occurred! Exiting.")
    cleanup_and_exit()

def clamp_speed(speed, min_speed, max_speed):
    """Clamp the speed to ensure it stays within min and max bounds."""
    return [max(min(s, max_speed), min_speed) for s in speed]

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

# Function to reset the timeout when user interacts with the screen
def reset_timer():
    global timer
    if timer:
        timer.cancel()  # Cancel the current timer
    timer = Timer(timeout_duration, on_timeout)  # Create a new timer
    timer.start()  # Start the new timer

# Function to display touch coordinates on the screen
def display_touch(x, y):
    lcd.fill(BLACK)
    draw_level1_buttons()  # Redraw buttons after clearing the screen
    touch_text = font_small.render(f'Touch at ({x}, {y})', True, WHITE)
    lcd.blit(touch_text, (80, 100))  # Display coordinates at center of screen
    pygame.display.update()

# Draw the Level 1 buttons
def draw_level1_buttons():
    pygame.draw.rect(lcd, WHITE, start_button_rect, 2)
    start_text = font_big.render('Start', True, WHITE)
    lcd.blit(start_text, (start_button_rect.x + 20, start_button_rect.y + 5))

    pygame.draw.rect(lcd, WHITE, quit_button_rect, 2)
    quit_text = font_big.render('Quit', True, WHITE)
    lcd.blit(quit_text, (quit_button_rect.x + 20, quit_button_rect.y + 5))

    pygame.display.update()
  # Draw the Level 2 buttons
def draw_level2_buttons():
    # Pause button
    pygame.draw.rect(lcd, WHITE, pause_button_rect, 2)
    pause_text = font_small.render('Pause', True, WHITE)
    lcd.blit(pause_text, (pause_button_rect.x + 5, pause_button_rect.y + 10))  # Adjusted for taller button

    # Faster button
    pygame.draw.rect(lcd, WHITE, faster_button_rect, 2)
    faster_text = font_small.render('Faster', True, WHITE)
    lcd.blit(faster_text, (faster_button_rect.x + 5, faster_button_rect.y + 10))  # Adjusted for taller button

    # Slower button
    pygame.draw.rect(lcd, WHITE, slower_button_rect, 2)
    slower_text = font_small.render('Slower', True, WHITE)
    lcd.blit(slower_text, (slower_button_rect.x + 5, slower_button_rect.y + 10))  # Adjusted for taller button

    # Back button
    pygame.draw.rect(lcd, WHITE, back_button_rect, 2)
    back_text = font_small.render('Back', True, WHITE)
    lcd.blit(back_text, (back_button_rect.x + 5, back_button_rect.y + 10))  # Adjusted for taller button

    pygame.display.update()

# Cleanup function for safe exit
def cleanup_and_exit():
    global running, exiting
    if exiting:
        return
    print("Exiting...")
    exiting = True
    if timer:
        timer.cancel()  # Cancel the timer if it's still running
    running = False
    try:
        pygame.quit()
        GPIO.cleanup()
    except Exception as e:
        print(f"Error during cleanup: {e}")
    os._exit(0)
def level2_menu():
    global animation_running, animation_paused, speed1, speed2
    animation_running = True
    lcd.fill(BLACK)
    pygame.display.update()
    
    while animation_running:
        pitft.update()
        draw_level2_buttons()

        # Check for touch events in the Level 2 menu
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if pause_button_rect.collidepoint(x, y):
                    if animation_paused:
                        print("Resuming animation")
                        animation_paused = False
                    else:
                        print("Pausing animation")
                        animation_paused = True

                elif faster_button_rect.collidepoint(x, y):
                    print("Faster button pressed")
                    # Increase speed by a factor and clamp the speed to the limits
                    speed1 = clamp_speed([s * SPEED_MULTIPLIER for s in speed1], MIN_SPEED, MAX_SPEED)
                    speed2 = clamp_speed([s * SPEED_MULTIPLIER for s in speed2], MIN_SPEED, MAX_SPEED)
                    print(f"New speed1: {speed1}, New speed2: {speed2}")
                
                elif slower_button_rect.collidepoint(x, y):
                    print("Slower button pressed")
                    # Decrease speed by a factor and clamp the speed to the limits
                    speed1 = clamp_speed([s / SPEED_MULTIPLIER for s in speed1], MIN_SPEED, MAX_SPEED)
                    speed2 = clamp_speed([s / SPEED_MULTIPLIER for s in speed2], MIN_SPEED, MAX_SPEED)
                    print(f"New speed1: {speed1}, New speed2: {speed2}")

                elif back_button_rect.collidepoint(x, y):
                    print("Back to Level 1 menu")
                    animation_running = False  # Stop the animation and return to Level 1

        if not animation_paused:
            # Handle the ball movement and collision
            handle_ball_movement()

        sleep(0.01)  # Reduce sleep to improve frame rate

    # Clear the screen before going back to Level 1
    lcd.fill(BLACK)
    draw_level1_buttons()  # Return to Level 1 
  

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

# Main loop for Level 1 menu
try:
    draw_level1_buttons()  # 画出 Level 1 的按钮
    reset_timer()  # 开始定时器（30秒无操作自动退出）

    while running:
        pitft.update()  # 更新 PiTFT 触摸事件

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # 如果点击了 Start 按钮
                if start_button_rect.collidepoint(x, y):
                    print("Start button pressed!")
                    level2_menu()  # 切换到 Level 2 菜单

                # 如果点击了 Quit 按钮
                elif quit_button_rect.collidepoint(x, y):
                    print("Quit button pressed!")
                    cleanup_and_exit()  # 退出程序

                # 如果点击了按钮以外的位置，则显示坐标
                else:
                    print(f"Touch at ({x}, {y})")
                    display_touch(x, y)  # 在 PiTFT 上显示触摸坐标

                # 每次点击后重置定时器
                reset_timer()

        # 处理 GPIO Bailout 按钮（接在 GPIO 17 上）
        if GPIO.input(BAILOUT_BUTTON_PIN) == GPIO.LOW:
            print("Bailout button detected!")
            cleanup_and_exit()

        sleep(0.01)  # 小延迟以减少 CPU 过度使用

except KeyboardInterrupt:
    cleanup_and_exit()  # 捕获键盘中断，安全退出