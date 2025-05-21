import os
import re
import requests
import subprocess
from typing import Optional
from applications.base import baseApplication
from utils.version import is_newer_version
from utils.downloader import download_file


class NotepadPlusPlus(baseApplication):
    def __init__(self):
        self.name = "Notepad++"
        self.download_url = "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.8.1/npp.8.8.1.Installer.exe"
        self.version_url = "https://notepad-plus-plus.org/downloads/"
        self.installer_path = os.path.join(os.getcwd(), "npp_installer.exe")

    def get_installed_version(self) -> str:
        try:
            # Registry query for Notepad++ (x64 path)
            result = subprocess.run(
                ['reg', 'query', r'HKEY_LOCAL_MACHINE\SOFTWARE\Notepad++', '/v', 'DisplayVersion'],
                capture_output=True, text=True
            )
            match = re.search(r"DisplayVersion\s+REG_SZ\s+([\d.]+)", result.stdout)
            if match:
                return match.group(1)
        except Exception as e:
            print(f"Error fetching installed version: {e}")
        return "Not Installed"

    def get_latest_version(self) -> str:
        try:
            response = requests.get(self.version_url)
            match = re.search(r"/downloads/([\d.]+)/", response.text)
            if match:
                return match.group(1)
        except Exception as e:
            print(f"Error fetching latest version: {e}")
        return "Unknown"

    def download_installer(self) -> str:
        try:
            if download_file(self.download_url, self.installer_path):
                return self.installer_path
            return ""
        except Exception as e: # Should ideally be caught by download_file, but as a fallback.
            print(f"Unexpected error during download_installer for Notepad++: {e}")
            return ""

    def needs_update(self) -> bool:
        installed_version = self.get_installed_version()
        latest_version = self.get_latest_version()

        if latest_version == "Unknown":
            print(f"Cannot determine the latest version for {self.name}. Update check skipped.")
            return False

        if installed_version == "Not Installed":
            # If a latest version is known, and it's not installed, it needs "updating" (i.e., installing)
            print(f"{self.name} is not installed. Installation recommended if latest version '{latest_version}' is desired.")
            return True

        return is_newer_version(latest_version, installed_version)

    def install_update(self, installer_path: str) -> bool:
        try:
            subprocess.run([installer_path, '/S'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Installer failed: {e}")
            return False
