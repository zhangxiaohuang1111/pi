#!/bin/bash
cd /home/pi 

python more_video_control_cb.py &

sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb1 mplayer -vo sdl -framedrop -input file=/home/pi/video_fifo bigbuckbunny320p.mp4
#mplayer -input file=/home/pi/video_fifo bigbuckbunny320p.mp4
