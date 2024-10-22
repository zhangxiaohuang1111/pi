import os

# Path to the FIFO file that mplayer is monitoring for commands
FIFO_PATH = "/home/pi/video_fifo"  # Adjust this to your actual FIFO file path

def send_command_to_mplayer(command):
    """Send the command to the mplayer instance via the FIFO."""
    if os.path.exists(FIFO_PATH):
        with open(FIFO_PATH, 'w') as fifo:
            fifo.write(command + '\n')
    else:
        print(f"FIFO file {FIFO_PATH} not found.")
        
def main():
    print("Enter a command (pause, quit):")

    while True:
        # Get user input
        user_input = input("> ").strip()

        # Recognize valid commands
        if user_input == "pause":
            send_command_to_mplayer("pause")
            print("Command 'pause' sent to mplayer.")
        elif user_input == "quit":
            print("Exiting script.")
            break
        else:
            print("Invalid command. Try 'pause' or 'quit'.")

if __name__ == "__main__":
    main()
