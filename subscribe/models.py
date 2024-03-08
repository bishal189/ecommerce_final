from django.db import models
from Category.models import Category
from account.models import Account
# Create your models here.
class SubscribeModel(models.Model):
    category=models.ForeignKey(Account,on_delete=models.CASCADE),
    subscribers=models.ManyToManyField(Category)
