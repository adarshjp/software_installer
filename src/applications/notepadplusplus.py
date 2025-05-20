import os
import re
import requests
import subprocess
from typing import Optional
from applications.base import baseApplication

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
            response = requests.get(self.download_url, stream=True)
            with open(self.installer_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return self.installer_path
        except Exception as e:
            print(f"Error downloading installer: {e}")
            return ""

    def install_update(self, installer_path: str) -> bool:
        try:
            subprocess.run([installer_path, '/S'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Installer failed: {e}")
            return False
