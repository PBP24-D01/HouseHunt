"""
URL configuration for HouseHunt project.py

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
from django.views.static import serve
from django.urls import path, include,re_path

from HouseHunt import settings

urlpatterns = [
    path('admin/', admin.site.urls), 
    path("", include("HouseHuntAuth.urls")),
    path('iklan/', include('iklan.urls')),
    path('cekrumah/', include('cekrumah.urls')),
    path("auction/", include("auction.urls")),
    path("", include("rumah.urls")),
    path("", include("wishlist.urls")),
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    path("diskusi/", include("diskusi.urls")),
]
