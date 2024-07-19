"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', include('django_prometheus.urls')),
    path('admin/', admin.site.urls),
	path("api/", include([
		path("auth/", include("ft_auth.urls")),
		path("user/", include("ft_user.urls")),
		path("game/", include("ft_game.urls")),
	    path("lounge/", include("ft_lounge.urls")),
		path("lobby/", include("ft_lobby.urls")),
		path("room/", include("ft_room.urls")),
	])),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)