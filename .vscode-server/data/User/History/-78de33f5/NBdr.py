import RPi.GPIO as GPIO
import time

# GPIO Pin Setup for Motor A and Motor B
AIN1 = 5  # Motor A Direction Pin 1
AIN2 = 6  # Motor A Direction Pin 2
BIN1 = 20 # Motor B Direction Pin 1
BIN2 = 21 # Motor B Direction Pin 2
PWMA = 16 # Motor A PWM Control
PWMB = 16 # Motor B PWM Control

# GPIO Pin Setup for Buttons
buttonA_control = 17  # 左轮顺时针和逆时针切换
buttonA_stop = 22     # 左轮停止按钮
buttonB_control = 23  # 右轮顺时针和逆时针切换
buttonB_stop = 27     # 右轮停止按钮
button_exit = 26      # 强制退出程序

# Setup GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

# Setup Button GPIOs
GPIO.setup(buttonA_control, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 上拉电阻
GPIO.setup(buttonA_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # 上拉电阻
GPIO.setup(buttonB_control, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 上拉电阻
GPIO.setup(buttonB_stop, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # 上拉电阻
GPIO.setup(button_exit, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # 上拉电阻

# Setup PWM
pwm_a = GPIO.PWM(PWMA, 50)  # 50Hz PWM for Motor A
pwm_b = GPIO.PWM(PWMB, 50)  # 50Hz PWM for Motor B
pwm_a.start(0)  # Initial duty cycle set to 0 (stopped)
pwm_b.start(0)

# 状态变量，用于记录当前电机的旋转方向
stateA = 0  # 0 = 停止, 1 = 顺时针, 2 = 逆时针
stateB = 0  # 0 = 停止, 1 = 顺时针, 2 = 逆时针

# Motor control functions
def motor_a_forward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    pwm_a.ChangeDutyCycle(50)  # Half speed

def motor_a_backward():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    pwm_a.ChangeDutyCycle(50)  # Half speed

def motor_a_stop():
    pwm_a.ChangeDutyCycle(0)

def motor_b_forward():
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    pwm_b.ChangeDutyCycle(50)  # Half speed

def motor_b_backward():
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    pwm_b.ChangeDutyCycle(50)  # Half speed

def motor_b_stop():
    pwm_b.ChangeDutyCycle(0)

# Button press handlers
def handle_buttonA_control(channel):
    global stateA
    if stateA == 0 or stateA == 2:  # 切换到顺时针
        motor_a_forward()
        print("Left motor forward")
        stateA = 1
    else:  # 切换到逆时针
        motor_a_backward()
        print("Left motor backward")
        stateA = 2

def handle_buttonA_stop(channel):
    global stateA
    motor_a_stop()
    print("Left motor stopped")
    stateA = 0

def handle_buttonB_control(channel):
    global stateB
    if stateB == 0 or stateB == 2:  # 切换到顺时针
        motor_b_forward()
        print("Right motor forward")
        stateB = 1
    else:  # 切换到逆时针
        motor_b_backward()
        print("Right motor backward")
        stateB = 2

def handle_buttonB_stop(channel):
    global stateB
    motor_b_stop()
    print("Right motor stopped")
    stateB = 0

def handle_exit(channel):
    print("Exiting program...")
    GPIO.cleanup()
    exit(0)

# Add event detection for buttons
GPIO.add_event_detect(buttonA_control, GPIO.FALLING, callback=handle_buttonA_control, bouncetime=300)
GPIO.add_event_detect(buttonA_stop, GPIO.FALLING, callback=handle_buttonA_stop, bouncetime=300)
GPIO.add_event_detect(buttonB_control, GPIO.FALLING, callback=handle_buttonB_control, bouncetime=300)
GPIO.add_event_detect(buttonB_stop, GPIO.FALLING, callback=handle_buttonB_stop, bouncetime=300)
GPIO.add_event_detect(button_exit, GPIO.FALLING, callback=handle_exit, bouncetime=300)

try:
    while True:
        # Continuously check for button presses
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    # Clean up GPIO pins
    pwm_a.stop()
    pwm_b.stop()
    GPIO.cleanup()