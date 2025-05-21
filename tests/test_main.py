import unittest
from unittest.mock import patch
import sys

class TestMain(unittest.TestCase):

    @patch("main.UpdateManager")
    def test_main_with_one_app(self, mock_manager):
        test_args = ["main.py", "--apps", "notepadplusplus"]
        with patch.object(sys, "argv", test_args):
            import main  # Re-import main with patched argv
            main.main()
            mock_manager.return_value.run_updates.assert_called_with(["notepadplusplus"])

    @patch("main.UpdateManager")
    def test_main_with_multiple_apps(self, mock_manager):
        test_args = ["main.py", "--apps", "notepadplusplus", "firefox"]
        with patch.object(sys, "argv", test_args):
            import main
            main.main()
            mock_manager.return_value.run_updates.assert_called_with(["notepadplusplus", "firefox"])
