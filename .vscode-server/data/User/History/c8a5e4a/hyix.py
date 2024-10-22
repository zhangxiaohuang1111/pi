import os
import RPi.GPIO as GPIO
import time

# Path to the FIFO file that mplayer is monitoring
FIFO_PATH = "/home/pi/video_fifo"  # Adjust to your actual FIFO file path

# Define GPIO pins for the buttons (replace with actual pin numbers)
BUTTON_PINS = {
    'pause': 17,       # Pause button GPIO pin
    'fast_forward': 22,  # Fast forward 10 seconds GPIO pin
    'rewind': 23,      # Rewind 10 seconds GPIO pin
    'quit': 27         # Quit mplayer GPIO pin
}

def send_command_to_mplayer(command):
    """Send the command to the mplayer instance via the FIFO."""
    if os.path.exists(FIFO_PATH):
        with open(FIFO_PATH, 'w') as fifo:
            fifo.write(command + '\n')
    else:
        print(f"FIFO file {FIFO_PATH} not found.")
        
def button_callback(channel):
    """Handle button presses and control mplayer actions."""
    if channel == BUTTON_PINS['pause']:
        print("Pause button pressed")
        send_command_to_mplayer("pause")
    elif channel == BUTTON_PINS['fast_forward']:
        print("Fast forward button pressed")
        send_command_to_mplayer("seek 10")
    elif channel == BUTTON_PINS['rewind']:
        print("Rewind button pressed")
        send_command_to_mplayer("seek -10")
    elif channel == BUTTON_PINS['quit']:
        print("Quit button pressed")
        send_command_to_mplayer("quit")
        GPIO.cleanup()
        exit()

def main():
    # Set GPIO numbering to Broadcom (BCM)
    GPIO.setmode(GPIO.BCM)
    
    # Set up each button pin as input with pull-up resistors and attach callback
    for pin in BUTTON_PINS.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=button_callback, bouncetime=300)
    
    print("Monitoring buttons for mplayer control.")
    
    try:
        # Keep the script running to monitor button presses
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
