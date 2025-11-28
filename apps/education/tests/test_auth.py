# Python modules
from rest_framework import status


def test_jwt_obtain(api, user):
    """Test JWT token obtain with valid credentials."""
    response = api.post('/api/token/', {'email': user.email, 'password': '12345'})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data

def test_jwt_obtain_bad_credentials(api, user):
    """Test JWT token obtain with invalid credentials."""
    response = api.post('/api/token/', {'email': user.email, 'password': 'wrong'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_jwt_refresh(api, user):
    """Test JWT token refresh with valid refresh token."""
    token_response = api.post('/api/token/', {'email': user.email, 'password': '12345'})
    assert token_response.status_code == status.HTTP_200_OK
    refresh_token = token_response.data['refresh']
    
    response = api.post('/api/token/refresh/', {'refresh': refresh_token})
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data

def test_jwt_refresh_bad_token(api):
    """Test JWT token refresh with invalid refresh token."""
    response = api.post('/api/token/refresh/', {'refresh': 'invalid_token'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


