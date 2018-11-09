import datetime
import os
import shutil
import unittest
from Common import get_string_date_from_file
from Common import set_date_to_file
from Common import set_date_to_file_from_string
from Common import get_date_from_string
from Common import get_date_from_file
from Common import get_string_iso_date_from_string
from Common import get_date_string_from_date
from Common import date_time_string_to_utc_date_time
from Common import utc_date_time_to_local_date_time_string
from printer import display_info


class MyTestCase(unittest.TestCase):
    def test_read_write_string_date(self):

        test_file = "test_file.txt"

        if os.path.exists(test_file):
            shutil.rmtree(test_file, ignore_errors=True)

        f = open(test_file, "w+")
        f.close()

        expected_date = "2017-12-23T11:29:37"
        print("expected date: " + expected_date)
        set_date_to_file_from_string(test_file, expected_date)
        actual_date = get_string_date_from_file(test_file)
        print("actual date: " + actual_date)
        self.assertEqual(expected_date, actual_date)

    def read_write_time(self):

        test_file = "test_file_1.txt"

        if os.path.exists(test_file):
            shutil.rmtree(test_file, ignore_errors=True)

        f = open(test_file, "w+")
        f.close()

        expected_date_string = "2017-12-23T11:29:37"
        expected_date = get_date_from_string(expected_date_string)
        set_date_to_file(test_file, expected_date)
        actual_date = get_date_from_file(test_file)
        self.assertEqual(expected_date, actual_date)

    def test_utc(self):

        expected_date_string = "2017-12-23T11:29:37"
        result_utc_time = date_time_string_to_utc_date_time(expected_date_string)
        local_date_time = utc_date_time_to_local_date_time_string(result_utc_time)
        self.assertEqual(expected_date_string, local_date_time)

    def test_utc(self):
        display_info("hallo")

if __name__ == '__main__':
    unittest.main()
