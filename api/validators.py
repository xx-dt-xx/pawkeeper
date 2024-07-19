from django.core.exceptions import ValidationError
import re


# Validate that the value provided contains letters only.
def validate_alpha(value):
    if not re.match(r'^[A-Za-z ]+$', value):
        raise ValidationError('This field should contain alphabetic characters and spaces only.')