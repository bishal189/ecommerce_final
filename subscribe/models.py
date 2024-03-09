from django.db import models
from Category.models import Category
from account.models import Account
# Create your models here.
class SubscribeModel(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    subscribers=models.ManyToManyField(Account)
