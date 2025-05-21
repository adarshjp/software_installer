import unittest
from utils.version import is_newer_version

class TestVersionUtils(unittest.TestCase):

    def test_newer_version_true(self):
        self.assertTrue(is_newer_version("1.2.0", "1.1.9"))

    def test_newer_version_false(self):
        self.assertFalse(is_newer_version("1.0.0", "1.2.5"))

    def test_equal_versions(self):
        self.assertFalse(is_newer_version("2.0.1", "2.0.1"))

    def test_invalid_versions(self):
        self.assertFalse(is_newer_version("abc", "1.0.0"))
