from django.db import models
from django.utils import timezone as django_timezone
from django.db.models import DateTimeField


class AbstractSoftDeletableModel(models.Model):
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

        
    def delete(self, *args: tuple[any, ...], **kwargs: dict[any, any]) -> None:
        self.deleted_at = django_timezone.now()
        self.save(update_fields=['deleted_at'])