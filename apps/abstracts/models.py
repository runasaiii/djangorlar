#Python modules
from typing import Any

#Django modules
from django.db.models import Model, DateTimeField
from django.utils import timezone as django_timezone


class AbstractBaseModel(Model):
    """Abstract base model with created and updated timestamps."""
    created_at = DateTimeField(
        auto_now_add=True
    )
    updated_at = DateTimeField(
        auto_now=True
    )
    deleted_at = DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True

    def delete(self, *args: tuple[Any, ...], **kwargs: dict[Any, Any]) -> None:
        self.deleted_at = django_timezone.now()
        self.save(update_fields=["deleted_at"])
