import unittest
from unittest.mock import patch, MagicMock
import subprocess  # Import the subprocess module
from applications.notepadplusplus import NotepadPlusPlus


class TestNotepadPlusPlus(unittest.TestCase):

    @patch("subprocess.run")
    def test_get_installed_version(self, mock_run):
        mock_output = "DisplayVersion    REG_SZ    8.5.1"
        mock_run.return_value = MagicMock(stdout=mock_output)

        app = NotepadPlusPlus()
        version = app.get_installed_version()

        self.assertEqual(version, "8.5.1")

    @patch("requests.get")
    def test_get_latest_version(self, mock_get):
        mock_response = MagicMock()
        # mock_response.text = '<a href="/downloads/8.6.5/">Latest Release</a>'
        # Ensure the mock HTML matches the regex's expectations
        # Specifically, the href should contain '/vX.Y.Z/' and the link text should contain 'Notepad++ vX.Y.Z'
        mock_response.text = '<a href="/downloads/v8.6.5/">Notepad++ v8.6.5</a>'
        mock_response.raise_for_status = (
            MagicMock()
        )  # Mock raise_for_status to prevent it from being an issue
        mock_get.return_value = mock_response

        app = NotepadPlusPlus()
        latest = app.get_latest_version()

        self.assertEqual(latest, "8.6.5")

    @patch("requests.get")
    @patch("builtins.open", new_callable=unittest.mock.mock_open)
    def test_download_installer(self, mock_open, mock_get):
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b"testdata"]
        mock_get.return_value = mock_response

        app = NotepadPlusPlus()
        path = app.download_installer()

        self.assertTrue(path.endswith("npp_installer.exe"))

    @patch("subprocess.run")
    def test_install_update_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)

        app = NotepadPlusPlus()
        result = app.install_update("fake_installer.exe")

        self.assertTrue(result)

    @patch(
        "subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1, cmd=["fake_installer.exe", "/S"]
        ),
    )
    def test_install_update_failure(self, mock_run):
        app = NotepadPlusPlus()
        result = app.install_update("fake_installer.exe")

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
