# Python modules
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Django modules
from django.urls import path, include

# Project modules
from .views import CourseViewSet, LessonViewSet
from apps.auths.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT view that uses email instead of username."""
    serializer_class = CustomTokenObtainPairSerializer


course_list = CourseViewSet.as_view({'get': 'list', 'post': 'create'})
course_detail = CourseViewSet.as_view({'get': 'retrieve', 'put': 'update','delete': 'delete'})
course_activate = CourseViewSet.as_view({'post': 'activate'})
course_deactivate = CourseViewSet.as_view({'post': 'deactivate'})
course_lessons = CourseViewSet.as_view({'get': 'lessons'})

lesson_create = LessonViewSet.as_view({'post': 'create'})
lesson_delete = LessonViewSet.as_view({'delete': 'delete'})
lesson_move = LessonViewSet.as_view({'put': 'move'})
lesson_publish = LessonViewSet.as_view({'post': 'publish'})
lesson_unpublish = LessonViewSet.as_view({'post': 'unpublish'})

urlpatterns = [
    #JWT Auth urls
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #Course urls
    path('api/v1/education/courses/', course_list, name='course-list'),
    path('api/v1/education/courses/<int:pk>/', course_detail, name='course-detail'),
    path('api/v1/education/courses/<int:pk>/activate/', course_activate, name='course-activate'),
    path('api/v1/education/courses/<int:pk>/deactivate/', course_deactivate, name='course-deactivate'),
    path('api/v1/education/courses/<int:pk>/lessons/', course_lessons, name='course-lessons'),
    #Lesson urls
    path('api/v1/education/lessons/', lesson_create, name='lesson-create'),
    path('api/v1/education/lessons/<int:pk>/', lesson_delete, name='lesson-delete'),
    path('api/v1/education/lessons/<int:pk>/move/', lesson_move, name='lesson-move'),
    path('api/v1/education/lessons/<int:pk>/publish/', lesson_publish, name='lesson-publish'),
    path('api/v1/education/lessons/<int:pk>/unpublish/', lesson_unpublish, name='lesson-unpublish'),
]