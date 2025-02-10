import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8 or len(password) > 20:
            raise ValidationError(
                _('Password must be between 8 and 20 characters long.'),
                code='password_too_short',
            )
        if not re.search('\d', password):
            raise ValidationError(
                _('Password must contain at least one digit.'),
                code='password_no_number',
            )
        if not re.search('[A-Za-z]', password):
            raise ValidationError(
                _('Password must contain at least one letter.'),
                code='password_no_letter',
            )
        if not re.search('[^A-Za-z0-9]', password):
            raise ValidationError(
                _('Password must contain at least one special character.'),
                code='password_no_special',
            )

    def get_help_text(self):
        return _('Password must be between 8 and 20 characters long, and include letters, numbers, and special characters.')
