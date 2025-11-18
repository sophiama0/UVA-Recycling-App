from django.urls import path

from . import views

urlpatterns = [
    path('', views.recycling_map, name='recycling-map'),
    path('post-recycling-location/', views.post_recycling_location, name='post-recycling-location'),
    path('bin/<int:pk>/update/', views.update_recycling_location, name='update-recycling-location'),
    path('bin/<int:pk>/', views.RecyclingBinDetailView.as_view(), name='recycling-bin-detail'),
    path('bin/<int:pk>/vote/', views.vote_bin, name='vote-bin'),
    path('bin/<int:pk>/recycle/', views.recycle_here, name='recycle-here'),
    path('bin/<int:pk>/recycle/update-fullness/', views.update_fullness_after_recycle, name='recycle-update-fullness'),
    path('community/', views.community, name='community'),
    path('profile/<str:first_name>_<int:user_id>', views.profile, name='recycling-profile'),
    path('settings/', views.settings, name='settings'),
    path("api/bins/", views.bin_locations, name="bin_locations"),
    path("map/", views.map_page, name="map"),
]