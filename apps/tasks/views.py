from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from .models import Project, Task


def home(request):
    return redirect("projects:list")


def projects_list(request):
    projects_qs = Project.objects.select_related("author").prefetch_related("users").order_by("id")
    paginator = Paginator(projects_qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tasks/projects_list.html", {"page_obj": page_obj})


def project_detail(request, pk: int):
    project = get_object_or_404(Project.objects.select_related("author"), pk=pk)
    tasks_qs = Task.objects.filter(project=project).order_by("id")
    paginator = Paginator(tasks_qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tasks/project_detail.html", {"project": project, "page_obj": page_obj})


def tasks_list(request):
    tasks_qs = Task.objects.select_related("project").order_by("id")
    paginator = Paginator(tasks_qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tasks/tasks_list.html", {"page_obj": page_obj})


def task_detail(request, pk: int):
    task = get_object_or_404(Task.objects.select_related("project"), pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task})
