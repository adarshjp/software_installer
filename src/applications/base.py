# Abstract Class for Applications
from abc import ABC, abstractmethod


class baseApplication(ABC):
    name: str
    version_url: str
    download_url: str
    installer_path: str

    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_installed_version(self) -> str:
        pass

    @abstractmethod
    def get_latest_version(self) -> str:
        pass

    @abstractmethod
    def download_installer(self) -> str:
        pass

    @abstractmethod
    def install_update(self, installer_path: str) -> bool:
        pass

    @abstractmethod
    def needs_update(self) -> bool:
        pass
