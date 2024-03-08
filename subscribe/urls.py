from django.urls import path
from . import views
urlpatterns=[
    path('add/',views.subscribe,name="subscribe"),
    path('remove/',views.unsubscribe,name="unsubscribe")
    ]
