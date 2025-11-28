# Django modules
from django.contrib import admin

# Project modules
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'is_active', 'created_at', 'updated_at', 'deleted_at')
    list_filter = ('is_active', 'created_at', 'owner')
    search_fields = ('title', 'description', 'owner__username', 'owner__email')
    ordering = ('-created_at',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'is_published', 'indentation', 'order', 'created_at', 'updated_at', 'deleted_at')
    list_filter = ('is_published', 'course', 'created_at')
    search_fields = ('title', 'content', 'course__title')
    ordering = ('course', 'order')