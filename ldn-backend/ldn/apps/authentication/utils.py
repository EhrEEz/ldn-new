from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email


def validate_email(value: str) -> tuple[bool, str]:
    """Validate a single email."""
    message_invalid = "Enter a valid email address."

    if not value:
        return False, message_invalid
    try:
        django_validate_email(value)
    except ValidationError:
        return False, message_invalid

    return True, ""
