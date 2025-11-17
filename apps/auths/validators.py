#Django modules
from django.core.exceptions import ValidationError

_RESTRICTED_DOMAINS = (
    "@mail.ru",
    "@yandex.ru",
)

def validate_email_domain(value: str) -> None:
    """Validate that the email belongs to a specific domain."""
    domain: str = value[value.index("@") :]
    if domain in _RESTRICTED_DOMAINS:
        raise ValidationError(
            message=f'Email must not be from one of the restricted domains: {", ".join(_RESTRICTED_DOMAINS)}',
            code='invalid_domain'
        )
    
def validate_username_no_special_chars(value: str) -> None:
    """Validate that the username does not contain special characters."""
    if not value.isalnum():
        raise ValidationError(
            message="Username must contain only alphanumeric characters.",
            code='invalid_username'
        )