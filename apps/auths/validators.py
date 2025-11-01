#Django modules
from django.core.exceptions import ValidationError

_RESTRICTED_DOMAINS = (
    "@mail.ru",
    "@yandex.ru",
    "@gmail.com",
)

def validate_email_domain(value: str):
    """Validate that the email belongs to a specific domain."""
    if not any(value.endswith(domain) for domain in _RESTRICTED_DOMAINS):
        raise ValidationError(
            message=f'Email must be from one of the allowed domains: {", ".join(_RESTRICTED_DOMAINS)}',
            code='invalid_domain'
        )