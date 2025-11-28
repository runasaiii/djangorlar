# Python modules
from rest_framework import status

# Project modules
from apps.education.models import Course


def test_course_creation(auth_api, user):
    response = auth_api.post('/api/v1/education/courses/', {
        'title': 'New Course',
        'description': 'Course Description'
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == 'New Course'

def test_course_list(auth_api, course):
    response = auth_api.get('/api/v1/education/courses/')
    assert response.status_code == 200
    assert len(response.data) == 1

def test_course_retrieve(auth_api, course):
    resp = auth_api.get(f'/api/v1/education/courses/{course.id}/')
    assert resp.status_code == 200
    assert resp.data['id'] == course.id

def test_course_update_only_owner(auth_api, course, user2):
    """Test that only owner can update a course."""
    auth_api.force_authenticate(user=user2)
    response = auth_api.put(f'/api/v1/education/courses/{course.id}/', {
        'title': 'Bad update',
        'description': 'Bad description',
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_course_soft_delete(auth_api, course):
    resp = auth_api.delete(f'/api/v1/education/courses/{course.id}/')
    assert resp.status_code == 204

    course.refresh_from_db()
    assert course.deleted_at is not None

def test_course_activate(auth_api, course):
    course.is_active = False
    course.save()

    resp = auth_api.post(f'/api/v1/education/courses/{course.id}/activate/')
    assert resp.status_code == 200
    assert resp.data['is_active'] is True

def test_course_deactivate(auth_api, course):
    resp = auth_api.post(f'/api/v1/education/courses/{course.id}/deactivate/')
    assert resp.status_code == 200
    assert resp.data['is_active'] is False

def test_course_creation_bad_data(auth_api):
    """Test course creation with missing required field."""
    response = auth_api.post('/api/v1/education/courses/', {
        'description': 'Course Description'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_course_list_with_query_params(auth_api, course):
    """Test course list with is_active query parameter."""
    # Test with is_active=true
    response = auth_api.get('/api/v1/education/courses/?is_active=true')
    assert response.status_code == 200
    assert len(response.data) >= 1
    
    # Test with is_active=false
    course.is_active = False
    course.save()
    response = auth_api.get('/api/v1/education/courses/?is_active=false')
    assert response.status_code == 200
    assert len(response.data) >= 1

def test_course_update_bad_data(auth_api, course):
    """Test course update with invalid data."""
    response = auth_api.put(f'/api/v1/education/courses/{course.id}/', {
        'title': '',  # Empty title should fail
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_course_activate_already_active(auth_api, course):
    """Test activating a course that is already active."""
    course.is_active = True
    course.save()
    resp = auth_api.post(f'/api/v1/education/courses/{course.id}/activate/')
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

def test_course_lessons_list(auth_api, course, lesson):
    """Test listing lessons of a course."""
    resp = auth_api.get(f'/api/v1/education/courses/{course.id}/lessons/')
    assert resp.status_code == 200
    assert len(resp.data) >= 1
    assert resp.data[0]['id'] == lesson.id