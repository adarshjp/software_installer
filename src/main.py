import argparse
from manager import UpdateManager

def parse_args():
    parser = argparse.ArgumentParser(
        description="Software Updater for Notepad++, Firefox, and MS Teams"
    )
    parser.add_argument(
        "--apps",
        nargs="+",
        choices=["notepadplusplus", "firefox", "msteams"],
        required=True,
        help="List of apps to check/update (e.g., --apps notepadplusplus firefox)"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    manager = UpdateManager()
    manager.run_updates(args.apps)

if __name__ == "__main__":
    main()
