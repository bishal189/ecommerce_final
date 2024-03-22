from django.core.mail import EmailMessage
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
    def register(self, subscribe,observer):
        pass

    def unregister(self,subscribe, observer):
        pass

    def notify(self,subscribe,subject,message):
        pass

class ConcreteObserver(Observer):
    def update(self,subject,message,email):
        print("In update,subject,message,email")
        send_email = EmailMessage(subject, message, to=[email])
        send_email.send()

class ConcreteSubject(Subject):
    #Here subscribe is an instance of SubscribeModel and observer is an instance of Account Model
    def register(self,subscribe, observer):
        print("attached")
        subscribe.subscribers.add(observer)

    def unregister(self,subscribe, observer):
        subscribe.subscribers.remove(observer)

    #Get all subscribers from subscribe(SubscribeModel Instance) and update observer to just send message
    def notify(self,subscribe,subject,message):
        for subscriber in subscribe.subscribers.all():
            observer=ConcreteObserver()
            observer.update(subject,message,subscriber.email)

