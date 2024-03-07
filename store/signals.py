# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Product
from account.models import Account
from django.core.mail import EmailMessage

@receiver(post_save, sender=Product)
def send_notification_to_users(sender, instance, created, **kwargs):
    print("some notification")
    if created:
        print("hello")
        subject = 'New Product Added'
        message = f"A new item '{instance.product_name}' has been added in greatStore. Check it out!"
        users = Account.objects.filter(is_active=True)
        print(users)
        for user in users:
            to_email=user.email
            send_email = EmailMessage(subject, message, to=[to_email])
            send_email.send()

