import unittest
from unittest.mock import patch, mock_open, MagicMock
from utils.downloader import download_file


class TestDownloader(unittest.TestCase):

    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_download_file_success(self, mock_open_func, mock_requests):
        mock_response = MagicMock()
        mock_response.iter_content = lambda chunk_size: [b"data"]
        mock_response.raise_for_status = lambda: None
        mock_requests.return_value = mock_response

        result = download_file("http://fake-url.com", "testfile.exe")
        self.assertTrue(result)

    @patch("requests.get", side_effect=Exception("Download failed"))
    def test_download_file_failure(self, mock_requests):
        result = download_file("http://bad-url.com", "fail.exe")
        self.assertFalse(result)
