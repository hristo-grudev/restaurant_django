from django.core.exceptions import ValidationError


def validate_only_letters(value):
    for ch in value:
        if not ch.isalpha():
            # Invalid case
            raise ValidationError('Value must contain only letters')
    # valid case
    #
    # if not all(ch.isalpha() for ch in value):
    #     raise ValidationError('Value must contain only letters')


