import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from . import models


# I learned how to do the following code from
# https://sixfeetup.com/blog/custom-password-validators-in-django
class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("The password must contain at least 1 symbol: " +
                  "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 symbol: " +
            "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter"),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):            
            raise ValidationError(
                _("The password must contain at least 1 digit."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )

class FirstnameValidator(object):
    def validate(self, password, user=None):        
            try:
                if re.findall(user.profile.first_name, password):
                    if user.profile.first_name == '':
                        pass
                    else:
                        raise ValidationError(
                        _("The password must not cantain your first name."),
                        code='password_first_name',
                    )
            except AttributeError:
                pass


    def get_help_text(self):
        return _(
            "The password must not cantain your first name."
        )


class LastnameValidator(object):
    def validate(self, password, user=None):        
        try:
            if re.findall(user.profile.last_name, password):
                if user.profile.last_name == '':
                    pass
                else:
                    raise ValidationError(
                        _("The password must not cantain your last name."),
                        code='password_last_name',
                    )
        except AttributeError:
            pass


    def get_help_text(self):
        return _(
            "The password must not cantain your last name."
        )


class UsernameValidator(object):
    def validate(self, password, user=None):
        try:
            if re.findall(user.username, password):
                if user.profile.first_name == '':
                    pass
                else:
                    raise ValidationError(
                        _("The password must not cantain your username."),
                        code='password_username',
                    )
        except AttributeError:
            pass

    def get_help_text(self):
        return _(
            "The password must not cantain your username."
        )