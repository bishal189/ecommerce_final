# interfaces.py

from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

class Subject:
    def attach(self, observer):
        pass

    def detach(self, observer):
        pass

    def notify(self):
        pass
