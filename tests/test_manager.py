import unittest
from unittest.mock import patch, MagicMock
from manager import UpdateManager


class TestUpdateManager(unittest.TestCase):

    def test_get_supported_apps(self):
        manager = UpdateManager()
        apps = manager.get_supported_apps()
        self.assertIn("notepadplusplus", apps)

    @patch(
        "manager.NotepadPlusPlus"
    )  # Patch where NotepadPlusPlus is looked up by UpdateManager
    @patch(
        "builtins.input", return_value="y"
    )  # Mock input to simulate user confirmation
    def test_run_updates_valid_app(
        self, mock_input, mock_NotepadPlusPlus_class_in_manager
    ):
        # Create a mock instance of NotepadPlusPlus
        mock_app_instance = MagicMock()
        mock_app_instance.name = "Notepad++"
        mock_app_instance.needs_update.return_value = (
            True  # Simulate that an update is required
        )
        mock_app_instance.download_installer.return_value = "dummy_path.exe"
        mock_app_instance.install_update.return_value = True

        # Configure the mocked class to return the mock instance
        mock_NotepadPlusPlus_class_in_manager.return_value = mock_app_instance

        # Create an instance of UpdateManager and run updates
        manager = UpdateManager()
        manager.run_updates(["notepadplusplus"])

        # Assertions
        mock_app_instance.needs_update.assert_called_once()  # Ensure needs_update was called
        mock_app_instance.download_installer.assert_called_once()  # Ensure download_installer was called
        mock_app_instance.install_update.assert_called_once_with(
            "dummy_path.exe"
        )  # Ensure install_update was called

    def test_run_updates_unknown_app(self):
        manager = UpdateManager()
        # No exception expected for unknown app
        manager.run_updates(["unknown_app"])  # Should print error, not crash
