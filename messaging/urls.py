from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('<str:first_name>_<int:user_id>/', views.chat, name='chat'),
    path('<str:first_name>_<int:user_id>/api', views.chat_messages_api, name='chat_messages_api'),
]
