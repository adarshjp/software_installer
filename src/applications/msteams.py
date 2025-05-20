import os
import re
import requests
import subprocess
from applications.base import baseApplication

class MSTeams(baseApplication):
    def __init__(self):
        self.name = "Microsoft Teams"
        self.version_url = "https://learn.microsoft.com/en-us/microsoftteams/teams-client-update"
        self.download_url = "https://statics.teams.cdn.office.net/production-windows-x64/enterprise/Teams_windows_x64.exe"
        self.installer_path = os.path.join(os.getcwd(), "teams_installer.exe")

    def get_installed_version(self) -> str:
        try:
            result = subprocess.run(
                ['reg', 'query', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Teams', '/v', 'Version'],
                capture_output=True, text=True
            )
            match = re.search(r"Version\s+REG_SZ\s+([\d.]+)", result.stdout)
            if match:
                return match.group(1)
        except Exception as e:
            print(f"Error fetching installed version: {e}")
        return "Not Installed"

    def get_latest_version(self) -> str:
        try:
            response = requests.get(self.version_url)
            # Extract something like "version 1.6.00.12345" from page
            match = re.search(r"version\s+([\d.]+)", response.text, re.IGNORECASE)
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
            subprocess.run([installer_path, '/quiet'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Installer failed: {e}")
            return False
