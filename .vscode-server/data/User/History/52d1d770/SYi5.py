import RPi.GPIO as GPIO
import time
import pygame
import os
import threading
import signal
import sys
import pigame  # 确保 pigame 模块正确安装
from pygame.locals import *

# 设置环境变量
os.putenv('SDL_VIDEODRV', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV', 'TSLIB')  # 使用 TSLIB 驱动
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')  # 使用触摸屏设备

# 初始化 PyGame 和 PiTFT
pygame.init()
pitft = pigame.PiTft(rotation=90)  # 初始化 PiTFT，确保 pigame 支持正确的旋转
screen = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible(True)  # 显示鼠标
font_small = pygame.font.Font(None, 17)

# GPIO 设置
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# GPIO 引脚设置
buttonA_control = 17
buttonA_stop = 22
buttonB_control = 23
buttonB_stop = 27
button_exit = 26

GPIO.setup(buttonA_control, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonA_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB_control, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# 主循环
running = True

# 显示更新函数
def update_display():
    global running
    try:
        while running:
            pitft.update()  # 更新 PiTFT 事件
            screen.fill(BLACK)

            # 显示按钮历史
            left_text = font_small.render("Left History", True, WHITE)
            screen.blit(left_text, (10, 10))

            right_text = font_small.render("Right History", True, WHITE)
            screen.blit(right_text, (170, 10))

            # 绘制 STOP 按钮
            pygame.draw.circle(screen, RED, (160, 120), 30)
            stop_text = font_small.render("STOP", True, WHITE)
            screen.blit(stop_text, (145, 115))

            # 绘制 QUIT 按钮
            pygame.draw.rect(screen, WHITE, (230, 180, 80, 40), 2)
            quit_text = font_small.render("QUIT", True, WHITE)
            screen.blit(quit_text, (250, 190))

            pygame.display.update()

            # 处理触摸事件
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    # 检查是否按下 STOP 按钮
                    if 130 <= x <= 190 and 90 <= y <= 150:
                        print("STOP button pressed - Both motors stopped")
                    
                    # 检查是否按下 QUIT 按钮
                    elif 230 <= x <= 310 and 180 <= y <= 220:
                        print("QUIT button pressed")
                        running = False  # 停止主循环
                        return

            time.sleep(0.1)
    except pygame.error as e:
        print(f"Pygame error: {e}")
    finally:
        pygame.quit()

# 启动显示线程
display_thread = threading.Thread(target=update_display, daemon=True)
display_thread.start()

# 主循环
try:
    while running:
        time.sleep(0.1)
except KeyboardInterrupt:
    running = False
finally:
    GPIO.cleanup()
    sys.exit(0)