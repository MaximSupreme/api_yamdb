from django.core.exceptions import ValidationError
from django.utils import timezone as tz


def validate_year(value):
    current_year = tz.now().year
    if value > current_year:
        raise ValidationError('The release year of the title'
                              'cannot be in the future')
