from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.catalogs.urls")),
    path("shop/", include("apps.commerces.urls")),
]
