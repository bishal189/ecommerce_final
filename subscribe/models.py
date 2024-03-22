from django.db import models
from Category.models import Category
from account.models import Account
from subscribe.interface import Observer,Subject
# Create your models here.
class SubscribeModel(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    subscribers=models.ManyToManyField(Account)


    def attach(self, observer):
        print("attached")
        self.subscribers.add(observer)

    def detach(self, observer):
        self.subscribers.remove(observer)

    def notify(self,subject,message):
        for subscriber in self.subscribers.all():
            subscriber.update(self,subject,message)
