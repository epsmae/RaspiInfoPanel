#!/usr/bin/env python

import io
import os
import time
from time import sleep
import RPi.GPIO as GPIO
import subprocess
import filecmp
from shutil import copyfile
import sys
import datetime
import termios
import tty
from select import select


VIDEO_PLAYER_BINARIES = '/home/pi/Documents/Infopanel/hello_pi/hello_video/hello_video.bin'
MEDIA_EXTERNAL_SOURCE = '/media/pi'
MEDIA_SOURCE = 'infopanel.h264'
MEDIA_SOURCE_PATH = '/home/pi/Documents/Infopanel/video_source/' + MEDIA_SOURCE
BOUNCE_TIME=400

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def display_info( str):
    now = datetime.datetime.now()
    print now.strftime("%Y-%m-%d %H:%M:%S") + " > " + str
    return

def print_supprocesses():
    current_process = psutil.Process()
    children = current_process.children(recursive=True)
    for child in children:
	display_info("child pid: " + str(child.pid))

def check_presentation():
    
    try:
       directoryList = os.listdir(MEDIA_EXTERNAL_SOURCE)

       if not directoryList:
          display_info("No USB device found")
       else:
          display_info("Following devices found: " + "\n".join(directoryList))
         
       for sub_directory in directoryList:
          path = os.path.join(MEDIA_EXTERNAL_SOURCE, sub_directory)
          presentation = os.path.join(path, MEDIA_SOURCE)
          if os.path.exists(presentation):
             if os.path.exists(MEDIA_SOURCE_PATH) and filecmp.cmp(presentation, MEDIA_SOURCE_PATH):
                display_info("Same presentation do not copy")
             else:
                display_info("Try copy file " + presentation + ' to ' + MEDIA_SOURCE_PATH + "...")
                try:
                   #copyfile(presentation, dest_directory)  
                   copyfile(presentation, MEDIA_SOURCE_PATH)               
                   display_info("...successful")
                except:
                   display_info("...failed" + sys.exc_info()[0])
          else:
             display_info("No " + MEDIA_SOURCE + " file available in: " + path)
    
    except:
       display_info("failed to check presentation")
    return

def callback_start(channel):
    global running
    display_info("Start detected")
    running = True

def callback_stop(channel):
    display_info("Stop detected")
    stop_video()

def callback_exit(channel):
    display_info("Exit detected")
    stop_video()
    GPIO.cleanup()
    sys.exit(0)

def callback_shutdown(channel):
    display_info("Shutdown detected")
    GPIO.cleanup()
    os.system('shutdown now -h')

def callback_reboot(channel):
    display_info("Reboot detected")
    GPIO.cleanup()
    os.system('shutdown now -r')

def callback_copy(channel):
    display_info("Copy detected")
    stop_video()
    check_presentation()

def stop_video():
    global myprocess
    global running

    if myprocess:
       display_info("stopping presentation...")
       myprocess.kill()
       res = myprocess.wait()
       display_info("exit code = " + str(res))
       display_info("...presentation stopped")
       myprocess = None

    running = False

	
#Program

display_info("Starting infopanel")

#Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)

myprocess = None

#initialize video state
running = True

GPIO.add_event_detect(7, GPIO.FALLING, callback=callback_shutdown, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(11, GPIO.FALLING, callback=callback_reboot, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(12, GPIO.FALLING, callback=callback_exit, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(13, GPIO.FALLING, callback=callback_copy, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(16, GPIO.FALLING, callback=callback_start, bouncetime=BOUNCE_TIME)
GPIO.add_event_detect(15, GPIO.FALLING, callback=callback_stop, bouncetime=BOUNCE_TIME)

display_info("Initialize complete")

# wait till raspi boot is complete and all usb devices detected
display_info("Starting in 20s...")
sleep(20)

check_presentation()

while True:
    
    sleep(1)
     
    timeout = 0.5
    rlist, _, _ = select([sys.stdin], [], [], timeout)
    if rlist:
        s = sys.stdin.read(1)
	if (s == "s"):
            callback_stop(0)

	if (s == "r"):
            callback_start(0)
	

    if myprocess or not running:
        sleep(0.1)
    else:
        display_info("Starting video loop")
        try:
           if os.path.exists(MEDIA_SOURCE_PATH):
              display_info("start playing video")
              myprocess = subprocess.Popen([VIDEO_PLAYER_BINARIES, MEDIA_SOURCE_PATH])
              display_info("proc id:" + str(myprocess.pid))           
           else:
              display_info("Video source file does not exist: " + source)
              sleep(10)
        except Exception as e:
           display_info("Unexpected error: " + str(e))
           sleep(10)

