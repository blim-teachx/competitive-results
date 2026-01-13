"""URL configuration for the competitive results website."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tournaments.urls")),
]
