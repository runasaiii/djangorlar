from django.urls import path
from . import views

app_name = "catalogs"

urlpatterns = [
    path("", views.restaurant_list, name="restaurant_list"),
    path("<int:pk>/", views.restaurant_detail, name="restaurant_detail"),
]
