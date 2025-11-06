from django.urls import path

from . import views

app_name = 'dashboard'


app_name = 'dashboard'

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/profile/", views.profile, name="account_profile"),
    path('inbox/', views.inbox, name='inbox'),
    path('chat/<str:username>/', views.chat, name='chat'),
    path('profile/', views.profile_view, name='profile'),
]