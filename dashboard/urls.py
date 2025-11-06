from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/profile/", views.profile, name="account_profile"),
    path('inbox', views.inbox, name='inbox'), 
    path('chat/<str:username>/', views.chat, name='chat'),
    path('inbox/', views.inbox, name ='inbox')
]