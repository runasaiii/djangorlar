from django.urls import path
from . import views


app_name = "projects"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.projects_list, name="list"),
    path("projects/<int:pk>/", views.project_detail, name="detail"),
    path("tasks/", views.tasks_list, name="tasks_list"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
]


