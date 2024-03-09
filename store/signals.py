# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Product
from account.models import Account
from django.core.mail import EmailMessage
from subscribe.models import SubscribeModel
@receiver(post_save, sender=Product)
def send_notification_to_users(sender, instance, created, **kwargs):
    if created:
        subject = 'New Product Added'
        message = f"A new item '{instance.product_name}' has been added in category {instance.category.category_name} in our greatStore. Check it out!"

        users =SubscribeModel.objects.get(category=instance.category)
        print(users)
        for user in users.subscribers.all():
            to_email=user.email
            print(to_email)
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()

