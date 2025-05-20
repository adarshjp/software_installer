#Abstract Class for Applications
from abc import ABC, abstractmethod

class baseApplication(ABC):
    @abstractmethod
    def get_installed_version(self)-> str:
        pass
    @abstractmethod
    def get_latest_version(self)-> str:
        pass
    @abstractmethod
    def download_installer(self)-> str:
        pass

    @abstractmethod
    def install_update(self)-> str:
        pass

    
    def needs_update(self)-> bool:
        self.get_installed_version()!= self.get_latest_version()