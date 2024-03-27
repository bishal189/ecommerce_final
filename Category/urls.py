# urls.py
from django.urls import path
from . import views

urlpatterns = [ 
    path('share/facebook/<int:pk>/', views.share_facebook, name='share_facebook'),
    # path('share/twitter/<int:pk>/', views.share_twitter, name='share_twitter'),
  
]
