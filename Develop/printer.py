import time
import datetime


def display_info(string):
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S") + " > " + string)
