from typing import Any
from random import choice, choices
from datetime import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import QuerySet

from apps.tasks.models import Task, Project, UserTask


class Command(BaseCommand):
    help = "Generate data for testing "

    EMAIL_DOMAINS = (
        "example.com",
        "test.com",
        "sample.org",
        "demo.net",
        "mail.com",
    )
    SOME_WORDS = (
        "moon",
        "sun",
        "star",
        "sky",
        "cloud",
        "rainbow",
        "rain",
        "snow",
        "wind",
        "storm",
        "thunder",
        "lightning",
        "breeze",
        "dawn",
        "dusk",
        "twilight",
        "eclipse",
        "comet",
        "planet",
        "galaxy",
        "nebula",
        "ocean",
        "sea",
        "wave",
        "river",
        "lake",
        "waterfall",
        "beach",
        "sand",
        "island",
        "mountain",
        "hill",
        "valley",
        "meadow",
        "forest",
        "tree",
        "flower",
        "leaf",
        "stone",
        "rock",
        "fire",
        "ember",
        "ash",
        "earth",
        "field",
        "garden",
        "path",
        "trail",
        "cave",
        "desert",
        "cliff",
        "rainforest",
        "prairie",
        "tundra",
        "cat",
        "dog",
        "bird",
        "fox",
        "wolf",
        "bear",
        "lion",
        "tiger",
        "zebra",
        "horse",
        "deer",
        "rabbit",
        "squirrel",
        "whale",
        "dolphin",
        "shark",
        "eagle",
        "owl",
        "bee",
        "butterfly",
        "ant",
        "frog",
        "fish",
        "turtle",
        "shell",
        " coral",
        "reef",
        "moss",
        "vine",
        "bamboo",
        "cactus",
        "acorn",
        "pine",
        "willow",
        "maple",
        "oak",
    )

    def __generate_users(self, user_count: int = 100) -> None:
        USER_PASSWORD = make_password(password="12345")
        created_users: list[User] = []
        users_before: int = User.objects.count()
        i: int
        for i in range(user_count):
            username: str = f"user {i+1}"
            email: str = f"user{i+1}@{choice(self.EMAIL_DOMAINS)}"
            created_users.append(
                User(
                    username=username,
                    email=email,
                    password=USER_PASSWORD,
                )
            )

        User.objects.bulk_create(created_users, ignore_conflicts=True)
        users_after: int = User.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {users_after - users_before} users."
            )
        )

    def __generate_projects(self, project_count: int = 100) -> None:
        create_projects: list[Project] = []
        projects_before: int = Project.objects.count()
        existed_users: QuerySet[User] = User.objects.all()

        i: int
        for i in range(project_count):
            name: str = " ".join(choices(self.SOME_WORDS, k=4)).capitalize()
            author: User = choice(existed_users)
            create_projects.append(
                Project(
                    name=name,
                    author=author
                )
            )
        Project.objects.bulk_create(create_projects, ignore_conflicts=True)

        project: Project
        for project in Project.objects.all():
            project.users.add(*choices(existed_users, k=10))

        projects_after: int = Project.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {projects_after - projects_before} projects."
            )
        )

    def __generate_tasks(self, tasks_per_project: int = 20) -> None:
        created_tasks: list[Task] = []
        tasks_before: int = Task.objects.count()
        projects: QuerySet[Project] = Project.objects.all()
        existed_users: QuerySet[User] = User.objects.all()

        project: Project
        for project in projects:
            i: int
            for i in range(tasks_per_project):
                title: str = " ".join(choices(self.SOME_WORDS, k=3)).capitalize()
                description: str = " ".join(choices(self.SOME_WORDS, k=10)).capitalize()
                status: int = choice([Task.STATUS_TODO, Task.STATUS_IN_PROGRESS, Task.STATUS_DONE])
                created_tasks.append(
                    Task(
                        title=title,
                        description=description,
                        status=status,
                        project=project,
                    )
                )

        Task.objects.bulk_create(created_tasks)

        # Assign users to tasks via through model
        created_tasks_qs: QuerySet[Task] = Task.objects.all()
        task: Task
        for task in created_tasks_qs:
            assignees = choices(existed_users, k=choice([0, 1, 2, 3]))
            user: User
            for user in assignees:
                UserTask.objects.get_or_create(task=task, custom_user=user)

        tasks_after: int = Task.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {tasks_after - tasks_before} tasks and assignments."
            )
        )

    def handle(self, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> None:
        start_time: datetime = datetime.now()

        self.__generate_users(user_count=500)
        self.__generate_projects(project_count=200)
        self.__generate_tasks(tasks_per_project=20)

        self.stdout.write(
            "The whole process to generate data took: {} seconds".format(
                (datetime.now() - start_time).total_seconds()
            )
        )