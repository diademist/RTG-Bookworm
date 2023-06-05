
import re
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from .models import StoredPassword
from django.utils.translation import ngettext

SALT = 'DLZjTiZxI1OE6pfFd9xVZwaaINK34JTF6BQdzb6bAPFFgUDgBneNiBwq6Oxs1upwe3MEr5R13pt3QFEbsuaPHDTroxsEGlIDyPBRhJd6jJTMg'

class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("The password must contain at least 1 special character: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 special character: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )


class RepeatedValidator(object):
    def validate(self, password, user=None):
        # In case there is no user this validator is not applicable, so we return success
        if user is None:
            return None

        hashed_password = make_password(password, salt=SALT)
        saved_password = StoredPassword.objects.filter(user=user, password=hashed_password).first()
        if saved_password is not None:
            raise ValidationError(
                _("The password cannot be the same as previously used passwords."),
                code='password_no_symbol',
            )

    def password_changed(self, password, user=None):
        # In case there is no user this is not applicable
        if user is None:
            return None

        hashed_password = make_password(password, salt=SALT)
        saved_password = StoredPassword.objects.filter(user=user, password=hashed_password).first()
        if saved_password is None:
            saved_password = StoredPassword()
            saved_password.user = user
            saved_password.password = hashed_password
            saved_password.save()

    def get_help_text(self):
        return _(
            "Your password cannot be the same as previously used passwords."
        )

class MaximumLengthValidator:
    """
    Validate whether the password is shorter than a maximum length.

    Parameters:
        max_length (int): the maximum number of characters to require in the password.
    """
    def __init__(self, max_length=75):
        self.max_length = max_length

    def validate(self, password, user=None):  # lint-amnesty, pylint: disable=unused-argument
        if len(password) > self.max_length:
            raise ValidationError(
                ngettext(
                    'This password is too long. It must contain no more than %(max_length)d character.',
                    'This password is too long. It must contain no more than %(max_length)d characters.',
                    self.max_length
                ),
                code='password_too_long',
                params={'max_length': self.max_length},
            )

    def get_help_text(self):
        return ngettext(
            'Your password must contain no more than %(max_length)d character.',
            'Your password must contain no more than %(max_length)d characters.',
            self.max_length
        ) % {'max_length': self.max_length}

    def get_restriction(self):
        """
        Returns a key, value pair for the restrictions related to the Validator
        """
        return 'max_length', self.max_length
