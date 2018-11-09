import os
import datetime

LOG_FOLDER = "Logs"


def display_info(string):
    now = datetime.datetime.now()
    text = now.strftime("%Y-%m-%d %H:%M:%S") + " > " + string
    print(text)

    try:
        if not os.path.exists(LOG_FOLDER):
            os.makedirs(LOG_FOLDER)

        full_file_path = os.path.join(LOG_FOLDER, "infopanel_" + now.strftime("%Y-%m-%d") + ".log")
        with open(full_file_path, "a") as logfile:
            logfile.writelines(text + "\n")
    except Exception as ex:
        print("print failed to write to log file: " + str(ex))
