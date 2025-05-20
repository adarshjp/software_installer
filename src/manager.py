from typing import List, Dict, Type
from applications.base import baseApplication
from applications.notepadplusplus import NotepadPlusPlus
from applications.firefox import Firefox
from applications.msteams import MSTeams

class UpdateManager:
    def __init__(self):
        self.app_registry: Dict[str, Type[baseApplication]] = {
            "notepadplusplus": NotepadPlusPlus,
            "firefox": Firefox,
            "msteams": MSTeams
        }

    def get_supported_apps(self) -> List[str]:
        return list(self.app_registry.keys())

    def run_updates(self, selected_apps: List[str]) -> None:
        summary = []

        for app_key in selected_apps:
            app_class = self.app_registry.get(app_key)
            if not app_class:
                print(f"Unknown application: {app_key}")
                continue

            app_instance = app_class()
            print(f"\n🔍 Checking {app_instance.name}...")

            installed_version = app_instance.get_installed_version()
            latest_version = app_instance.get_latest_version()

            print(f"Installed Version: {installed_version}")
            print(f"Latest Version:    {latest_version}")

            if installed_version == "Not Installed":
                print(f"ℹ️ {app_instance.name} is not installed.")
                summary_status = "Not Installed"
            elif installed_version == latest_version:
                print("✅ Already up to date.")
                summary_status = "Up to date"
            else:
                print("⬇️  Update available.")
                response = input(f"Do you want to update {app_instance.name} from {installed_version} to {latest_version}? (y/n): ").lower()

                if response == 'y' or response == 'yes':
                    print("Downloading installer...")
                    installer_path = app_instance.download_installer()

                    if installer_path:
                        print("Installing update...")
                        success = app_instance.install_update(installer_path)
                        if success:
                            print("✅ Update installed successfully.")
                            summary_status = "Update Successful"
                        else:
                            print("❌ Update failed.")
                            summary_status = "Update Failed"
                    else:
                        print("❌ Failed to download installer.")
                        summary_status = "Download Failed"
                else:
                    print("⏭️  Update skipped.")
                    summary_status = "Update Skipped"

            summary.append({
                "App": app_instance.name,
                "Installed": installed_version,
                "Latest": latest_version,
                "Status": summary_status
            })

        print("\n📝 Summary:")
        for item in summary: # Corrected loop variable name
            print(f"{item['App']}: Installed - {item['Installed']} | Latest - {item['Latest']} | Status - {item['Status']}")
