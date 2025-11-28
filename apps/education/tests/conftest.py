# Python modules
import pytest
from rest_framework.test import APIClient
from decimal import Decimal

# Django modules
from django.contrib.auth import get_user_model

# Project modules
from apps.education.models import Course, Lesson

User = get_user_model()


@pytest.fixture
def api():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        email='aruna@test.com',
        username='aruna',
        password='12345',
        full_name='Aruna Test'
    )

@pytest.fixture
def user2():
    return User.objects.create_user(
        email='test@test.com',
        username='test',
        password='12345',
        full_name='Test User'
    )

@pytest.fixture
def auth_api(api, user):
    api.force_authenticate(user=user)
    return api

@pytest.fixture
def course(user):
    return Course.all_objects.create(
        title='Test Course',
        description='A course for testing',
        owner=user
    )

@pytest.fixture
def lesson(course):
    return Lesson.all_objects.create(
        course=course,
        title='Test Lesson',
        content='Lesson content',
        indentation=0,
        order=Decimal('1'),
        is_published=False
    )