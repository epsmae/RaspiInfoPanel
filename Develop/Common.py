import datetime
import os
import time


class VersionInfo:
    def __init__(self):
        self.success = False


def get_string_date_from_file(file_path):
    date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
    return date


def get_string_iso_date_from_string(date_string):
    date_time = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S').isoformat()
    return date_time


def get_date_from_string(date_string):
    date_time = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
    return date_time


def get_date_from_file(file_path):
    date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    return date


def get_date_string_from_date(date_time):
    return date_time.strftime('%Y-%m-%dT%H:%M:%S')


def set_date_to_file(file_path, date_time):
    time_obj = time.mktime(date_time.timetuple())
    os.utime(file_path, (time_obj, time_obj))


def set_date_to_file_from_string(file_path, date_string):
    date_time_obj = datetime.datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')
    time_obj = time.mktime(date_time_obj.timetuple())
    os.utime(file_path, (time_obj, time_obj))


def date_time_string_to_utc_date_time(date_time_string):
    utc_offset = datetime.datetime.utcnow() - datetime.datetime.now()
    local_date_time = get_date_from_string(date_time_string)
    return local_date_time + utc_offset


def utc_date_time_to_local_date_time_string(utc_date_time):
    utc_offset = datetime.datetime.utcnow() - datetime.datetime.now()
    new_result_utc_time = utc_date_time - utc_offset;
    return get_date_string_from_date(new_result_utc_time)
