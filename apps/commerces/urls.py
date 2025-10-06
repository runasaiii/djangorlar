from django.urls import path
from . import views

app_name = "commerces"

urlpatterns = [
    path("", views.cart_view, name="cart_view"),
]
