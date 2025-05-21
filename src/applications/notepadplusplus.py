import os
import re
import requests
import subprocess
from bs4 import BeautifulSoup
from applications.base import baseApplication
from utils.version import is_newer_version
from utils.downloader import download_file
from elevate import elevate


class NotepadPlusPlus(baseApplication):
    def __init__(self) -> None:  # Already had -> None, but ensuring it's consistent
        self.name = "Notepad++"
        self.version_url = "https://notepad-plus-plus.org/downloads/"
        # Initialize download_url; it will be updated by get_latest_version
        self.download_url = ""
        self.installer_path = os.path.join(os.getcwd(), "npp_installer.exe")

    def get_installed_version(self) -> str:
        try:
            # Registry query for Notepad++ (x64 path)
            result = subprocess.run(
                [
                    "reg",
                    "query",
                    r"HKEY_LOCAL_MACHINE\SOFTWARE\Notepad++",
                    "/v",
                    "DisplayVersion",
                ],
                capture_output=True,
                text=True,
            )
            print(f"Registry query output: {result.stdout}")  # Debugging output

            # Match the DisplayVersion value in the registry output
            match = re.search(r"DisplayVersion\s+REG_SZ\s+([\d.]+)", result.stdout)
            if match:
                return match.group(1)

            # Fallback: Check the installation directory
            exe_path = r"C:\Program Files\Notepad++\notepad++.exe"
            if os.path.exists(exe_path):
                # Use the file's metadata to get the version
                import win32api
                info = win32api.GetFileVersionInfo(exe_path, "\\")
                ms = info["FileVersionMS"]
                ls = info["FileVersionLS"]
                version = f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"
                return version
        except Exception as e:
            print(f"Error fetching installed version for {self.name}: {e}")
        return "Not Installed"

    def get_latest_version(self) -> str:
        try:
            response = requests.get(self.version_url)
            response.raise_for_status()  # Check for HTTP errors

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the first <a> tag with an href containing "/downloads/v"
            link = soup.find("a", href=re.compile(r"/downloads/v([\d\.]+)/"))
            if link:
                # Extract the version number from the href
                match = re.search(r"/downloads/v([\d\.]+)/", link["href"])
                if match:
                    latest_version_str = match.group(1)

                    # Construct the download URL for the 64-bit installer
                    self.download_url = f"https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v{latest_version_str}/npp.{latest_version_str}.Installer.x64.exe"
                    return latest_version_str
        except requests.exceptions.RequestException as e:
            print(f"Error fetching latest version page for {self.name}: {e}")
        except Exception as e:
            print(f"Error processing latest version for {self.name}: {e}")

        self.download_url = ""  # Ensure download_url is cleared on error
        return "Unknown"

    def download_installer(self) -> str:
        try:
            if download_file(self.download_url, self.installer_path):
                return self.installer_path
            return ""
        except ValueError as e:  # Catch if self.download_url is empty or invalid
            print(f"Cannot download {self.name}: {e}")
            return ""
        except (
            Exception
        ) as e:  # Should ideally be caught by download_file, but as a fallback.
            print(f"Unexpected error during download_installer for Notepad++: {e}")
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
            # Elevate privileges for the installer
            elevate(graphical=False)  # Prevent opening a new terminal
            subprocess.run([installer_path, "/S"], check=True, timeout=300)  # Timeout after 5 minutes
            return True
        except subprocess.TimeoutExpired:
            print(f"Installer timed out for {self.name}.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Installer failed: {e}")
            return False
