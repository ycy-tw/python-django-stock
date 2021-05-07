from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class CustomizePasswordValidator():

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):

        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"

        if (len(password) < 8) \
                or (password.isalpha()) \
                or (password.isnumeric()) \
                or (password in special_characters):
            raise ValidationError(_('請輸入8位數以上英文和數字組合'))

    def get_help_text(self):
        return ""
