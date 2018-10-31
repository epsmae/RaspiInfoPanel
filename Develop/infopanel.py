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
from printer import display_info
from web_updater import download_update
from web_updater import check_for_update
from usb_updater import update_available

VIDEO_PLAYER_BINARIES = '/home/pi/Documents/Infopanel/hello_pi/hello_video/hello_video.bin'
MEDIA_EXTERNAL_SOURCE = '/media/pi'
MEDIA_SOURCE = 'infopanel.h264'
MEDIA_SOURCE_PATH = '/home/pi/Documents/Infopanel/video_source/' + MEDIA_SOURCE
ZIP_EXTRACT_FOLDER = "Download";
DOWNLOAD_SOURCE_PATH = '/home/pi/Documents/Infopanel/' + ZIP_EXTRACT_FOLDER + '/' + MEDIA_SOURCE

BOUNCE_TIME = 400
INPUT_TIMEOUT = 0.5


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


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
    check_for_usb_update()


def is_update_required(remote_date):
    try:
        date = datetime.datetime.fromtimestamp(os.path.getmtime(MEDIA_SOURCE_PATH)).isoformat()
        display_info("local date: " + date)
        display_info("remote date: " + remote_date)

        return remote_date > date
    except Exception as ex:
        display_info("failed to check if upate required: " + str(ex))
    return False


def check_for_web_update():
    try:

        display_info("check for web update...")
        res = check_for_update(ZIP_EXTRACT_FOLDER)
        if res.success and is_update_required(res.creation_date):
            display_info("...update required")
            res = download_update(ZIP_EXTRACT_FOLDER, res)
            if res.success:
                display_info("update download successful")
                copyfile(res.file_path, MEDIA_SOURCE_PATH)
                display_info("replaced video file")
            else:
                display_info("update download failed")
        else:
            display_info("...no update required")
    except Exception as ex:
        display_info(str(ex))


def check_for_usb_update():
    try:

        display_info("check for usb update...")
        res = update_available(MEDIA_EXTERNAL_SOURCE, MEDIA_SOURCE)
        if res.success and is_update_required(res.creation_date):
            display_info("...update required")
            copyfile(res.file_path, MEDIA_SOURCE_PATH)
        else:
            display_info("...no update required")
    except Exception as ex:
        display_info(str(ex))


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


def setup_gpio():
    # Setup GPIO pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(7, GPIO.FALLING, callback=callback_shutdown, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(11, GPIO.FALLING, callback=callback_reboot, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(12, GPIO.FALLING, callback=callback_exit, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(13, GPIO.FALLING, callback=callback_copy, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(16, GPIO.FALLING, callback=callback_start, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(15, GPIO.FALLING, callback=callback_stop, bouncetime=BOUNCE_TIME)


# Program

display_info("Starting infopanel")

setup_gpio()

myprocess = None
running = True

# wait till raspi boot is complete and all usb devices detected, internet available
display_info("Starting in 20s...")
sleep(20)

check_for_usb_update()
check_for_web_update()
sleep(5)
display_info("lets go")

while True:
    rlist, _, _ = select([sys.stdin], [], [], INPUT_TIMEOUT)
    if rlist:
        s = sys.stdin.read(1)
        if s == "s":
            callback_stop(0)

        if s == "r":
            callback_start(0)

        if s == "w":
            callback_stop(0)
            check_for_web_update()
            callback_start(0)

        if s == "u":
            callback_stop(0)
            check_for_usb_update()
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
                display_info("Video source file does not exist: " + MEDIA_SOURCE_PATH)
                sleep(10)
        except Exception as e:
            display_info("Unexpected error: " + str(e))
            sleep(10)
