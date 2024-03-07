from django.apps import AppConfig
# apps.py


from django.db.models import BigAutoField

class MyappConfig(AppConfig):
    default_auto_field = BigAutoField


class CategoryConfig(AppConfig):
    name = 'Category'
