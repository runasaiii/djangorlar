from django.contrib import admin
from .models import (
    Restaurant,
    Category,
    Option,
    MenuItem,
    ItemCategory,
    ItemOption,
)

admin.site.register([
    Restaurant,
    Category,
    Option,
    MenuItem,
    ItemCategory,
    ItemOption,
])
