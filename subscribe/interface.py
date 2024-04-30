# interfaces.py

from abc import ABC, abstractmethod
#self is not mandatory it was used because those impl were previously used in models

#Implement ABC(Absctract base class with update method that sends message implementation in class.py)
class Observer(ABC):
    @abstractmethod
    def update(self,subject,message,email):
        pass
#Abstract class for attaching,detaching and notifying observer based on subscribe model
class Subject:
    def attach(self, subscribe,observer):
        pass

    def detach(self,subscribe, observer):
        pass

    def notify(self,subscribe,subject,message):
        pass
