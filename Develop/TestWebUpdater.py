import unittest
from web_updater import check_for_update
from web_updater import download_update
from Common import VersionInfo


class MyTestCase(unittest.TestCase):
    def test_update(self):
        res = check_for_update("Download")
        self.assertEqual(res.success, True)
        self.assertEqual(res.creation_date is None, False)
        self.assertEqual(res.file_path is None, False)
        self.assertEqual(res.user_name is None, False)
        self.assertEqual(res.password is None, False)

    def test_download(self):
        info = VersionInfo()
        info.file_path = "https://my-update-domain.com/infopanel.zip"
        info.user_name = "username"
        info.password = "password"

        res = download_update("Download", info)
        self.assertEqual(res.success, True)
        self.assertEqual(res.creation_date is None, False)
        self.assertEqual(res.file_path is None, False)


if __name__ == '__main__':
    unittest.main()
