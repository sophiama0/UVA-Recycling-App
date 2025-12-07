"""
URL configuration for project_b_04 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from recycling.views import user_login_cancelled

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recycling.urls')),
    path('messages/', include('messaging.urls', namespace='messaging')),
    path('accounts/3rdparty/login/cancelled/', user_login_cancelled, name='account_login_cancelled'),
    path('accounts/', include('allauth.urls')),
    path('accounts/logout/', LogoutView.as_view(next_page='/'), name='account_logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)