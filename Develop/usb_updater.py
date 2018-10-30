import os
import sys
import filecmp
import datetime
from printer import display_info
from shutil import copyfile
from Common import VersionInfo


# MEDIA_EXTERNAL_SOURCE = '/media/pi'
# MEDIA_SOURCE = 'infopanel.h264'
# MEDIA_SOURCE_PATH = '/home/pi/Documents/Infopanel/video_source/' + MEDIA_SOURCE


def check_presentation(external_source_folder, local_source_full_file_name, source_file_name):

    try:
        directory_list = os.listdir(external_source_folder)

        if not directory_list:
            display_info("No USB device found")
        else:
            display_info("Following devices found: " + "\n".join(directory_list))

        for sub_directory in directory_list:
            path = os.path.join(external_source_folder, sub_directory)
            presentation = os.path.join(path, source_file_name)
            if os.path.exists(presentation):
                if os.path.exists(local_source_full_file_name) and filecmp.cmp(presentation,
                                                                               local_source_full_file_name):
                    display_info("Same presentation do not copy")
                else:
                    display_info("Try copy file " + presentation + ' to ' + local_source_full_file_name + "...")
                    try:
                        copyfile(presentation, local_source_full_file_name)
                        display_info("...successful")
                    except:
                        display_info("...failed" + sys.exc_info()[0])
            else:
                display_info("No " + source_file_name + " file available in: " + path)

    except:
        display_info("failed to check presentation")
    return


def update_available(external_source_folder, source_file_name):
    info = VersionInfo()

    try:
        directory_list = os.listdir(external_source_folder)

        if not directory_list:
            display_info("No USB device found")
            return info
        else:
            display_info("Following devices found: " + "\n".join(directory_list))

        for sub_directory in directory_list:
            path = os.path.join(external_source_folder, sub_directory)
            presentation = os.path.join(path, source_file_name)
            if os.path.exists(presentation):
                info.success = True
                info.file_path = presentation
                info.creation_date = datetime.datetime.fromtimestamp(os.path.getmtime(presentation))

    except Exception as ex:
        display_info("failed to check for usb update: " + str(ex))

    return info
