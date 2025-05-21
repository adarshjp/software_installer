import argparse
import ctypes
import sys
import os
from manager import UpdateManager
from elevate import elevate


def is_admin() -> bool:
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Software Updater for Notepad++, Firefox, and MS Teams"
    )
    parser.add_argument(
        "--apps",
        nargs="+",
        choices=["notepadplusplus", "firefox", "msteams", "all"],
        required=True,
        help="List of apps to check/update (e.g., --apps notepadplusplus firefox) or use 'all' to update all apps",
    )
    return parser.parse_args()


def main() -> None:
    # Check for administrative privileges
    if not is_admin():
        print("This script requires administrative privileges. Elevating...")
        elevate(graphical=False)  # Elevate the entire script
        print("Re-launching the script with administrative privileges...")
        os.execv(sys.executable, [sys.executable] + sys.argv)  # Re-launch the script
        return  # Exit the current process after re-launching

    args = parse_args()
    manager = UpdateManager()

    # Handle the 'all' option
    if "all" in args.apps:
        apps_to_update = manager.get_supported_apps()
    else:
        apps_to_update = args.apps

    manager.run_updates(apps_to_update)

    # Pause before exiting to allow the user to review the summary
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
