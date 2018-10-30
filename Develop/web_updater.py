import requests
import os.path
import time
import json
import datetime
import zipfile
import shutil
from printer import display_info
from Common import VersionInfo

current_video_path = "/video_source/infopanel.h264"
name_file_path = "product_name.txt"
server_file_path = "update_server.txt"


def remove(path):
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)


def get_request(url, username, password):
    if username == "" or password == "":
        return requests.get(url)
    else:
        return requests.get(url, auth=(username, password))


def check_and_download(zip_extract_folder):
    display_info("remove temporary data")

    zip_file_path = zip_extract_folder + "/" + "infopanel.zip"
    version_info_path = zip_extract_folder + "/" + "available_versions.json"

    # remove if there is some temporary data
    remove(zip_file_path)
    remove(version_info_path)
    remove(zip_extract_folder)

    if not os.path.exists(zip_extract_folder):
        os.makedirs(zip_extract_folder)

    display_info("get product info")
    # get product name
    with open(name_file_path, 'r') as name_file:
        global product
        product = name_file.readline()
        display_info("product: " + product)

    display_info("get server info")
    with open(server_file_path, 'r') as server_file:
        url_info = server_file.readline().split()
        version_url = url_info[0]

        if len(url_info) >= 3:
            username = url_info[1]
            password = url_info[2]
        else:
            username = ""
            password = ""

        display_info("url: " + version_url)

    # download version info
    version_request = get_request(version_url, username, password)
    display_info("status: " + str(version_request.status_code))

    if version_request.status_code != 200:
        raise ConnectionError("Failed to get version info, status code: " + str(version_request.status_code))

    with open(version_info_path, 'wb') as version_info:
        version_info.write(version_request.content)

    # parse version from json
    json_data = open(version_info_path)
    data = json.load(json_data)

    version = data["product"][product]["Version"]
    display_info("version: " + version)

    version_date = data["product"][product]["Datum"]
    display_info("version date: " + version_date)

    video_url = data["product"][product]["Url"]

    display_info("url: " + video_url)
    json_data.close()

    date_time_obj = datetime.datetime.strptime(version_date, '%Y-%m-%dT%H:%M:%S.%f')
    display_info("remote video iso time: " + date_time_obj.isoformat())

    # read current version date
    current_date_time_obj = datetime.datetime.fromtimestamp(os.path.getmtime(os.getcwd() + "/" + current_video_path))

    display_info("local video iso time: " + current_date_time_obj.isoformat())

    # check if version is newer
    if date_time_obj > current_date_time_obj:
        display_info("do update")
        display_info("dowloading zip")

        file_request = get_request(video_url, username, password)

        if file_request.status_code != 200:
            raise ConnectionError("Failed to download video, status code: " + str(file_request.status_code))

        with open(zip_file_path, 'wb') as zipFile:
            zipFile.write(file_request.content)

        # extract zip file, set date as the creation date is used in the infopanel
        display_info("extracting zip to " + zip_extract_folder)
        zip_ref = zipfile.ZipFile(zip_file_path, 'r')
        for zi in zip_ref.infolist():
            zip_ref.extract(zi, zip_extract_folder)
            date_time = time.mktime(zi.date_time + (0, 0, -1))
            os.utime(zip_extract_folder + "/" + zi.filename, (date_time, date_time))
            zip_ref.close()

        display_info("extracted zip")
        return 200
    else:
        print("do not update")
        return -1


def check_for_update(zip_extract_folder):
    result = VersionInfo()

    try:
        display_info("remove temporary data")

        zip_file_path = zip_extract_folder + "/" + "infopanel.zip"
        version_info_path = zip_extract_folder + "/" + "available_versions.json"

        # remove if there is some temporary data
        remove(zip_file_path)
        remove(version_info_path)
        remove(zip_extract_folder)

        if not os.path.exists(zip_extract_folder):
            os.makedirs(zip_extract_folder)

        display_info("get product info")
        # get product name
        with open(name_file_path, 'r') as name_file:
            global product
            product = name_file.readline()
            display_info("product: " + product)

        display_info("get server info")
        with open(server_file_path, 'r') as server_file:
            url_info = server_file.readline().split()
            version_url = url_info[0]

            if len(url_info) >= 3:
                username = url_info[1]
                password = url_info[2]
            else:
                username = ""
                password = ""

            display_info("url: " + version_url)

        # download version info
        version_request = get_request(version_url, username, password)
        display_info("status: " + str(version_request.status_code))

        if version_request.status_code != 200:
            raise ConnectionError("Failed to get version info, status code: " + str(version_request.status_code))

        with open(version_info_path, 'wb') as version_info:
            version_info.write(version_request.content)

        # parse version from json
        json_data = open(version_info_path)
        data = json.load(json_data)

        version = data["product"][product]["Version"]
        display_info("version: " + version)

        version_date = data["product"][product]["Datum"]
        display_info("version date: " + version_date)

        video_url = data["product"][product]["Url"]

        display_info("url: " + video_url)
        json_data.close()

        date_time_obj = datetime.datetime.strptime(version_date, '%Y-%m-%dT%H:%M:%S.%f')
        display_info("remote video iso time: " + date_time_obj.isoformat())

        result.creation_date = date_time_obj.isoformat()
        result.file_path = video_url
        result.user_name = username
        result.password = password
        result.success = True

    except Exception as ex:
        display_info("failed to check for usb update: " + str(ex))

    return result


def download_update(zip_extract_folder, info):
    result = VersionInfo()

    display_info("remove temporary data")

    zip_file_path = os.path.join(zip_extract_folder, "infopanel.zip")
    if not os.path.exists(zip_extract_folder):
        os.makedirs(zip_extract_folder)

    try:

        # remove if there is some temporary data
        remove(zip_file_path)

        if not os.path.exists(zip_extract_folder):
            os.makedirs(zip_extract_folder)

        display_info("do update")
        display_info("dowloading zip")

        file_request = get_request(info.file_path, info.user_name, info.password)

        if file_request.status_code != 200:
            raise ConnectionError("Failed to download video, status code: " + str(file_request.status_code))

        with open(zip_file_path, 'wb') as zipFile:
            zipFile.write(file_request.content)

        # extract zip file, set date as the creation date is used in the infopanel
        display_info("extracting zip to " + zip_extract_folder)
        zip_ref = zipfile.ZipFile(zip_file_path, 'r')
        for zi in zip_ref.infolist():
            zip_ref.extract(zi, zip_extract_folder)
            date_time = time.mktime(zi.date_time + (0, 0, -1))
            result.file_path = os.path.join(zip_extract_folder, zi.filename)
            os.utime(result.file_path, (date_time, date_time))
        zip_ref.close()

        result.success = True

        display_info("extracted zip")

    except Exception as ex:
        display_info("failed to check for usb update: " + str(ex))

    return result
