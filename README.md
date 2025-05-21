# Software Installer

A command-line utility to check for updates, download, and silently install/update specific Windows applications.

## Description

This project provides a simple way to manage installations and updates for a predefined list of software on a Windows system. It automates the process of:

1.  Checking the currently installed version of an application.
2.  Fetching the latest available version of the application from its official source.
3.  Comparing versions to determine if an update is needed.
4.  Downloading the installer for the latest version.
5.  Silently installing the downloaded application.

## Features

*   Automated version checking (installed vs. latest).
*   Downloads installers directly from official sources.
*   Silent installation of applications to avoid user prompts.
*   Modular design, making it easy to add support for new applications.
*   Basic logging for download and installation processes.

## Supported Applications

Currently, the following applications are supported:

*   Mozilla Firefox
*   Notepad++
*   Microsoft Teams

## Prerequisites

*   Windows Operating System
*   Python 3.7+
*   `pip` (Python package installer)

## Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone https://github.com/adarshjp/software_installer.git
    cd software_installer
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows CMD
    venv\Scripts\activate.bat
    # On Windows PowerShell
    .\venv\Scripts\Activate.ps1
    # On Git Bash / Linux / macOS
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The primary way to use this tool is likely through a main script (e.g., `main.py` or `manager.py`) that orchestrates the update process for specified applications.


**Example (conceptual):**

To check and update Notepad++:
```bash
python main.py notepadplusplus
```

To check and update all supported applications:
```bash
python main.py firefox notepadplusplus msteams
# or
python main.py --all
```



## Running Tests

To run the automated tests, ensure `pytest` is installed in your virtual environment and then execute:

```bash
pytest tests
```

## Project Structure

*   `src/applications/`: Contains modules for each supported application (e.g., `firefox.py`).
*   `src/utils/`: Contains utility modules like `downloader.py` and `version.py`.
*   `tests/`: Contains unit tests for the application and utility modules.
*   `main.py` / `manager.py`: (Assumed) Entry point and/or core logic for managing updates.

