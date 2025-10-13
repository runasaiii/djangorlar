# Django Modules
from django.contrib.admin import ModelAdmin, register

# Local Modules
from .models import Task, UserTask, Project


@register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'created_at',
    )
    list_display_links = (
        'id',
        'name',
    )
    list_per_page = 20
    search_fields = (
        'name',
    )
    ordering = (
        '-created_at',
        '-updated_at',
    )
    list_filter = (
        'author',
        'created_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'deleted_at',
    )

@register(Task)
class TaskAdmin(ModelAdmin):
    list_display = (
        'id',
        'title',
        'status',
        'project',
        'created_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'deleted_at',
    )
    list_filter = (
        'status',
    )


@register(UserTask)
class UserTaskAdmin(ModelAdmin):
    list_display = (
        'id',
        'task',
        'user',
        'created_at',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'deleted_at',
    )