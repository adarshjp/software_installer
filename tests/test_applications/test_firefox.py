import unittest
from unittest.mock import patch, MagicMock
import subprocess # Import the subprocess module
from applications.firefox import Firefox

class TestFirefox(unittest.TestCase):

    @patch("subprocess.run")
    def test_get_installed_version(self, mock_run):
        mock_run.return_value = MagicMock(stdout="CurrentVersion    REG_SZ    126.0")
        app = Firefox()
        version = app.get_installed_version()
        self.assertEqual(version, "126.0")

    @patch("requests.get")
    def test_get_latest_version(self, mock_get):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.json.return_value = {
            "LATEST_FIREFOX_VERSION": "126.0.1"
        }
        mock_get.return_value = mock_response

        app = Firefox()
        version = app.get_latest_version()
        self.assertEqual(version, "126.0.1")

    @patch("requests.get")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_download_installer(self, mock_open, mock_get):
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b'testdata']
        mock_get.return_value = mock_response

        app = Firefox()
        path = app.download_installer()
        self.assertTrue(path.endswith("firefox_installer.exe"))

    @patch("subprocess.run")
    def test_install_update_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        app = Firefox()
        result = app.install_update("dummy_path.exe")
        self.assertTrue(result)

    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(
        returncode=1,
        cmd=['dummy_path.exe', '/silent']
    ))
    def test_install_update_failure(self, mock_run):
        app = Firefox()
        result = app.install_update("dummy_path.exe")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
