import os
import re
import requests
import subprocess
from applications.base import baseApplication
from utils.version import is_newer_version
from utils.downloader import download_file


class Firefox(baseApplication):
    def __init__(self) -> None:
        self.name = "Firefox"
        self.version_url = (
            "https://product-details.mozilla.org/1.0/firefox_versions.json"
        )
        self.download_url = (
            "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"
        )
        self.installer_path = os.path.join(os.getcwd(), "firefox_installer.exe")

    def get_installed_version(self) -> str:
        try:
            result = subprocess.run(
                [
                    "reg",
                    "query",
                    r"HKEY_LOCAL_MACHINE\SOFTWARE\Mozilla\Mozilla Firefox",
                    "/v",
                    "CurrentVersion",
                ],
                capture_output=True,
                text=True,
            )
            match = re.search(r"CurrentVersion\s+REG_SZ\s+([\d.]+)", result.stdout)
            if match:
                return match.group(1)
        except Exception as e:
            print(f"Error fetching installed version: {e}")
        return "Not Installed"

    def get_latest_version(self) -> str:
        try:
            response = requests.get(self.version_url)
            if response.ok:
                data = response.json()
                return data.get("LATEST_FIREFOX_VERSION", "Unknown")
        except Exception as e:
            print(f"Error fetching latest version: {e}")
        return "Unknown"

    def download_installer(self) -> str:
        try:
            if download_file(self.download_url, self.installer_path):
                return self.installer_path
            return ""
        except (
            Exception
        ) as e:  # Should ideally be caught by download_file, but as a fallback.
            print(f"Unexpected error during download_installer for Firefox: {e}")
            return ""

    def needs_update(self) -> bool:
        installed_version = self.get_installed_version()
        latest_version = self.get_latest_version()

        if latest_version == "Unknown":
            print(
                f"Cannot determine the latest version for {self.name}. Update check skipped."
            )
            return False

        if installed_version == "Not Installed":
            # If a latest version is known, and it's not installed, it needs "updating" (i.e., installing)
            print(
                f"{self.name} is not installed. Installation recommended if latest version '{latest_version}' is desired."
            )
            return True

        return is_newer_version(latest_version, installed_version)

    def install_update(self, installer_path: str) -> bool:
        try:
            subprocess.run([installer_path, "/silent"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Installer failed: {e}")
            return False
