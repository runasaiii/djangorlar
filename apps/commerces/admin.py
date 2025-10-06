from django.contrib import admin
from .models import (
    Address,
    Order,
    OrderItem,
    OrderItemOption,
    PromoCode,
    OrderPromo,
)

admin.site.register([
    Address,
    Order,
    OrderItem,
    OrderItemOption,
    PromoCode,
    OrderPromo,
    ])
