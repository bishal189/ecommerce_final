from django.urls import path
from . import views
urlpatterns=[
    path('add/<category_id>/',views.subscribe,name="subscribe"),
    path('remove/<category_id>/',views.unsubscribe,name="unsubscribe")
    ]
