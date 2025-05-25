"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from station.admin import custom_admin_site
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Route pour obtenir le token
    TokenRefreshView,     # Route pour rafraîchir le token
)

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Inclus les URLs pour l'authentification
    path('stations/', include('station.urls')),  # Inclure les routes de l'application station
    path('api/',include('station.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtenir un token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Rafraîchir le token
]
    








