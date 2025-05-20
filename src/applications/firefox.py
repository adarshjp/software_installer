import os
import re
import requests
import subprocess
from applications.base import baseApplication

class Firefox(baseApplication):
    def __init__(self):
        self.name = "Firefox"
        self.version_url = "https://product-details.mozilla.org/1.0/firefox_versions.json"
        self.download_url = "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"
        self.installer_path = os.path.join(os.getcwd(), "firefox_installer.exe")

    def get_installed_version(self) -> str:
        try:
            result = subprocess.run(
                ['reg', 'query', r'HKEY_LOCAL_MACHINE\SOFTWARE\Mozilla\Mozilla Firefox', '/v', 'CurrentVersion'],
                capture_output=True, text=True
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
            subprocess.run([installer_path, '/silent'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Installer failed: {e}")
            return False
