import unittest
from unittest.mock import patch, MagicMock
import subprocess  # Import the subprocess module
from applications.msteams import MSTeams


class TestMSTeams(unittest.TestCase):

    @patch("subprocess.run")
    def test_get_installed_version(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Version    REG_SZ    1.6.00.12345")
        app = MSTeams()
        version = app.get_installed_version()
        self.assertEqual(version, "1.6.00.12345")

    @patch("requests.get")
    def test_get_latest_version(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "The latest version is version 1.6.00.13001 available now"
        mock_get.return_value = mock_response

        app = MSTeams()
        version = app.get_latest_version()
        self.assertEqual(version, "1.6.00.13001")

    @patch("requests.get")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_download_installer(self, mock_open, mock_get):
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b"teamsdata"]
        mock_get.return_value = mock_response

        app = MSTeams()
        path = app.download_installer()
        self.assertTrue(path.endswith("teams_installer.exe"))

    @patch("subprocess.run")
    def test_install_update_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        app = MSTeams()
        result = app.install_update("teams_installer.exe")
        self.assertTrue(result)

    @patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1,
            cmd=[
                "teams_installer.exe",
                "/quiet",
            ],  # Assuming '/quiet' is the silent flag for Teams
        ),
    )
    def test_install_update_failure(self, mock_run):
        app = MSTeams()
        result = app.install_update("teams_installer.exe")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
