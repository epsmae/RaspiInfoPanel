import unittest
import os
from usb_updater import update_available


class MyTestCase(unittest.TestCase):
    def test_update_sub_folder(self):
        external_source_folder = os.path.join(os.getcwd(), "TestData", "sub_folder")
        file_name = "infopanel.h264"

        res = update_available(external_source_folder, file_name)
        self.assertEqual(res.success, True)
        self.assertEqual(res.creation_date is None, False)
        self.assertEqual(res.file_path is None, False)

    def test_update_top_folder(self):
        external_source_folder = os.path.join(os.getcwd(), "TestData", "top_folder")
        file_name = "infopanel.h264"

        res = update_available(external_source_folder, file_name)
        self.assertEqual(res.success, True)
        self.assertEqual(res.creation_date is None, False)
        self.assertEqual(res.file_path is None, False)


if __name__ == '__main__':
    unittest.main()
