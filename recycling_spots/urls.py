from django.urls import path
from . import views 

urlpatterns = [
    # When someone visits /create/, call the create_spot_view function
    path('create/', views.create_spot_view, name='create_spot'),

    # When someone visits /spots/, call the spot_list_view function
    path('spots/', views.spot_list_view, name='spot_list'),
]