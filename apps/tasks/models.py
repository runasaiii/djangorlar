#Python modules

#Django modules
from django.db.models import (
    CharField,
    IntegerField,
    TextField,
    ForeignKey,
    ManyToManyField,
    UniqueConstraint,
    CASCADE,
    PROTECT,
)

#Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.auths.models import CustomUser


class Task(AbstractBaseModel):
    """Model representing a task within a project."""
    STATUS_TODO = 1
    STATUS_IN_PROGRESS = 2
    STATUS_DONE = 3
    STATUS_CHOICES = [
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DONE, 'Done'),
    ]

    NAME_MAX_LENGTH = 100

    title = CharField(
        max_length=NAME_MAX_LENGTH,
        db_index=True,
    )
    description= TextField(
        blank=True,
        default=''
    )
    status= IntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_TODO
    )
    project = ForeignKey(
        to = "Project",
        on_delete = CASCADE,
    )
    assignees = ManyToManyField(
        to=CustomUser,
        through="UserTask",
        through_fields=("task", "custom_user"),
        blank=True,
    )


class Project(AbstractBaseModel):
    NAME_MAX_LENGTH = 100
    name = CharField(
        max_length=NAME_MAX_LENGTH,
    )
    author = ForeignKey(
        to = CustomUser,
        on_delete = PROTECT,
        related_name = "projects",
    )
    users = ManyToManyField(
        to = CustomUser,
        blank = True,
        related_name = "projects_collaborated",
    )

    def __repr__(self) -> str:
        return f"Project(id={self.id}, name={self.name})" 
    
    def __str__(self):
        return self.name
    
class UserTask(AbstractBaseModel):
    task = ForeignKey(
        to = Task, 
        on_delete=CASCADE
        )
    custom_user = ForeignKey(
        to = CustomUser, 
        on_delete=CASCADE
        )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields = ["task", "custom_user"],
                name = "unique_task_user_assignment"
            )
        ]