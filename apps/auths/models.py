#Python modules

#Django modules
from django.db.models import(
    EmailField,
    CharField,
    BooleanField
) 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

#Project modules
from apps.abstracts.models import AbstractSoftDeletableModel
from apps.auths.validators import validate_email_domain


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractSoftDeletableModel):
    EMAIL_MAX_LENGTH = 255
    USERNAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 128
    email = EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        db_index=True,
        verbose_name="Email Address",
        help_text="Enter a valid email address.",
        validators=[validate_email_domain],
        )
    username = CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name="Username",
        help_text="Enter a unique username."
        )
    is_active = BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this user should be treated as active."
    )
    password = CharField(
        max_length=PASSWORD_MAX_LENGTH,
        verbose_name="Password",
        help_text="Enter a secure password."
    )
    is_staff = BooleanField(
        default=False,
        verbose_name="Staff",
        help_text="Designates whether this user can log into this admin site."
    )
    
    def __str__(self):
        return self.email
    
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']