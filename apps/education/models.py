# Django modules
from django.db import models
from django.db.models.functions import Now
from django.conf import settings
from django.utils import timezone

# Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.auths.models import CustomUser
from decimal import Decimal


class SoftDeleteQuerySet(models.QuerySet):
    """Custom QuerySet to handle soft deletion."""
    def delete(self):
        return super().update(deleted_at=Now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def dead(self):
        return self.exclude(deleted_at__isnull=True)
    
class SoftDeleteManager(models.Manager):
    """Custom Manager to use SoftDeleteQuerySet."""
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

class Course(models.Model):
    """Model representing an educational course."""
    TITLE_MAX_LENGTH = 200
    DESCRIPTION_MAX_LENGTH = 1000

    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        db_index=True,
    )
    description = models.TextField(
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
        default='',
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_courses',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    deleted_at = models.DateTimeField(
        null=True,  
        blank=True,
        default=None,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager() 

    class Meta:
        ordering = ['-created_at']

    def soft_delete(self):
        """Soft delete the course by setting deleted_at timestamp."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])
    

class Lesson(models.Model):
    """Model representing a lesson within a course."""
    TITLE_MAX_LENGTH = 200

    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name='lessons',
    )
    title = models.CharField(
        max_length=TITLE_MAX_LENGTH,
        db_index=True,
    )
    content = models.TextField()
    indentation = models.PositiveSmallIntegerField(
        default=0,
    )
    order = models.DecimalField(
        max_digits=12,
        decimal_places=6,
    )
    is_published = models.BooleanField(
        default=False,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    deleted_at = models.DateTimeField(
        null=True,  
        blank=True,
        default=None,
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['order']


    def save(self, *args, **kwargs):
        """Override save to set order and indentation on creation."""
        if not self.pk:
            first = (
                Lesson.objects.filter(course=self.course, deleted_at__isnull=True)
                .order_by('-order')
                .first()
            )
            if first is None:
                self.order = Decimal(0)
            else:
                self.order = Decimal(first.order) - Decimal('1')

            if self.indentation is None:
                self.indentation = 0
            if self.indentation > 5:
                self.indentation = 5
        super().save(*args, **kwargs)


    def soft_delete(self):
        """Soft delete the lesson by setting deleted_at timestamp."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])


    def __str__(self):
        return f"{self.title} (course={self.course_id})"