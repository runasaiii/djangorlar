#Python modules
from typing import Any

#Django modules
from django.db.models import(
    EmailField,
    CharField,
    BooleanField,
    DateField,
    DateTimeField,
    DecimalField,
) 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone

#Project modules
from apps.abstracts.models import AbstractBaseModel
from apps.auths.validators import (
    validate_email_domain,
    validate_username_no_special_chars
)


class CustomUserManager(BaseUserManager):
    """Custom user manager to handle user creation and superuser creation."""
    def __obtain_user_instance(
            self,
            email: str,
            username: str,
            full_name: str,
            password: str,
            **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        if not email:
            raise ValidationError(
                "The Email field must be set,",
                code = 'email_not_set'
            )
        if not full_name:
            raise ValidationError(
                "The Full Name field must be set,",
                code = 'full_name_not_set'
            )
        
        new_user: CustomUser = self.model(
            email = self.normalize_email(email),
            username = username,
            full_name = full_name,
            **kwargs
        )
        new_user.set_password(password)
        return new_user
    
    def create_user(
            self,
            email: str,
            username: str,
            full_name: str,
            password: str,
            **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email = email,
            username = username,
            full_name = full_name,
            password = password,
            **kwargs
        )
        # Password is already set in __obtain_user_instance, no need to set again
        new_user.save(using=self._db)
        return new_user
    
    def create_superuser(
            self,
            email: str,
            username: str,
            full_name: str,
            password: str,
            **kwargs: dict[str, Any]
    ) -> 'CustomUser':
        new_user: 'CustomUser' = self.__obtain_user_instance(
            email = email,
            username = username,
            full_name = full_name,
            password = password,
            is_staff = True,
            is_superuser = True,
            **kwargs
        )
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user


class CustomUser(AbstractBaseUser, PermissionsMixin, AbstractBaseModel):
    """Custom user model extending AbstractBaseUser and PermissionsMixin."""
    EMAIL_MAX_LENGTH = 100
    USERNAME_MAX_LENGTH = 150
    PASSWORD_MAX_LENGTH = 128
    FULL_NAME_MAX_LENGTH = 200

    ROLE_ADMIN = 'admin'
    ROLE_MANAGER = 'manager'
    ROLE_EMPLOYEE = 'employee'
    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_MANAGER, 'Manager'),
        (ROLE_EMPLOYEE, 'Employee'),
    ]

    first_name = CharField(
        max_length=30,
        verbose_name="First Name",
        help_text="Enter the first name of the user.",
        blank=True,
    )
    last_name = CharField(
        max_length=30,
        verbose_name="Last Name",
        help_text="Enter the last name of the user.",
        blank=True,
    )
    email = EmailField(
        unique=True,
        max_length=EMAIL_MAX_LENGTH,
        db_index=True,
        validators=[validate_email_domain],
        verbose_name="Email Address",
        help_text="Enter a valid email address.",
    )
    username = CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name="Username",
        help_text="Enter a unique username."
    )
    full_name = CharField(
        max_length=FULL_NAME_MAX_LENGTH,
        verbose_name="Full Name",
        help_text="Enter the full name of the user.",
        blank=True,
    )
    phone = CharField(
        max_length=15,
        verbose_name="Phone Number",
        help_text="Enter the phone number of the user.",
        null=True,
        blank=True,
    )
    country = CharField(
        max_length=50,
        verbose_name="Country",
        help_text="Enter the country of the user.",
        null=True,
        blank=True,
    )
    city = CharField(
        max_length=50,
        verbose_name="City",
        help_text="Enter the city of the user.",
        null=True,
        blank=True,
    )
    department = CharField(
        max_length=100,
        verbose_name="Department",
        help_text="Enter the department of the user.",
        null=True,
        blank=True,
    )
    role = CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_EMPLOYEE,
        verbose_name="Role",
        help_text="Select the role of the user.",
        null=True,
        blank=True,
    )
    birth_date = DateField(
        null=True,
        blank=True,
        verbose_name="Birth Date",
        help_text="Enter the birth date of the user.",
    )
    salary = DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Salary",
        help_text="Enter the salary of the user.",
    )
    # Note: password field is provided by AbstractBaseUser, no need to define it
    is_staff = BooleanField(
        default=False,
        verbose_name="Staff",
        help_text="Designates whether this user can log into this admin site."
    )
    is_active = BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this user should be treated as active."
    )
    date_joined = DateTimeField(
        default=timezone.now,
        verbose_name="Date Joined",
        help_text="The date and time when the user joined."
    )
    last_login = DateTimeField(
        null=True,
        blank=True,
        verbose_name="Last Login",  
        help_text="The date and time of the user's last login."
    )
    
    def __str__(self):
        return self.email
    
    REQUIRED_FIELDS = ['username', 'full_name']
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        ordering = ['-created_at']

    def clean(self) -> None:
        """Custom clean method to validate username."""
        validate_username_no_special_chars(self.username)
        return super().clean()


