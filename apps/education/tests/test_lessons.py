# Python modules
from rest_framework import status
from decimal import Decimal

# Project modules
from apps.education.models import Lesson


def test_lesson_creation(auth_api, course):
    response = auth_api.post('/api/v1/education/lessons/', {
        'course': course.id,
        'title': 'New Lesson',
        'content': 'Lesson Content',
        'indentation': 0,
    })
    assert response.status_code == 201
    assert response.data['title'] == 'New Lesson'

def test_lesson_creation_not_owner(api, course, user2):
    api.force_authenticate(user=user2)
    resp = api.post('/api/v1/education/lessons/', {
        'course': course.id,
        'title': 'Bad Lesson',
        'content': 'Bad Content',
        })
    assert resp.status_code == status.HTTP_403_FORBIDDEN

def test_lesson_soft_delete(auth_api, lesson):
    resp = auth_api.delete(f'/api/v1/education/lessons/{lesson.id}/')
    assert resp.status_code == 204
    lesson.refresh_from_db()
    assert lesson.deleted_at is not None


def test_lesson_publish(auth_api, lesson):
    resp = auth_api.post(f'/api/v1/education/lessons/{lesson.id}/publish/')
    assert resp.status_code == 200
    assert resp.data['is_published'] is True

def test_lesson_unpublish(auth_api, lesson):
    lesson.is_published = True
    lesson.save()

    resp = auth_api.post(f'/api/v1/education/lessons/{lesson.id}/unpublish/')
    assert resp.status_code == 200
    assert resp.data['is_published'] is False

def test_lesson_move(auth_api, lesson, course):
    #just move to the end
    resp = auth_api.put(f'/api/v1/education/lessons/{lesson.id}/move/', {}, format='json')
    assert resp.status_code == 200
    assert Decimal(resp.data['order']) >= 0

def test_lesson_move_before(auth_api, lesson, course):
    second = Lesson.all_objects.create(
        course=course,
        title='Second Lesson',
        content='Second Content',
        indentation=0,
        order=Decimal('10.0'),
    )

    resp = auth_api.put(f'/api/v1/education/lessons/{second.id}/move/', {
        'before_lesson_id': lesson.id}, format='json')
    assert resp.status_code == 200
    assert Decimal(resp.data['order']) < lesson.order

def test_lesson_creation_bad_data(auth_api, course):
    """Test lesson creation with missing required fields."""
    response = auth_api.post('/api/v1/education/lessons/', {
        'course': course.id,
        'content': 'Lesson Content',
        # title
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_lesson_creation_invalid_indentation(auth_api, course):
    """Test lesson creation with invalid indentation value."""
    response = auth_api.post('/api/v1/education/lessons/', {
        'course': course.id,
        'title': 'New Lesson',
        'content': 'Lesson Content',
        'indentation': 10, 
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_lesson_delete_not_owner(api, lesson, user2):
    """Test deleting a lesson by non-owner."""
    api.force_authenticate(user=user2)
    resp = api.delete(f'/api/v1/education/lessons/{lesson.id}/')
    assert resp.status_code == status.HTTP_403_FORBIDDEN

def test_lesson_publish_not_owner(api, lesson, user2):
    """Test publishing a lesson by non-owner."""
    api.force_authenticate(user=user2)
    resp = api.post(f'/api/v1/education/lessons/{lesson.id}/publish/')
    assert resp.status_code == status.HTTP_403_FORBIDDEN

def test_lesson_move_not_owner(api, lesson, user2):
    """Test moving a lesson by non-owner."""
    api.force_authenticate(user=user2)
    resp = api.put(f'/api/v1/education/lessons/{lesson.id}/move/', {}, format='json')
    assert resp.status_code == status.HTTP_403_FORBIDDEN

def test_lesson_move_invalid_before_id(auth_api, lesson, course):
    """Test moving a lesson with invalid before_lesson_id."""
    resp = auth_api.put(f'/api/v1/education/lessons/{lesson.id}/move/', {
        'before_lesson_id': 99999
    }, format='json')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST