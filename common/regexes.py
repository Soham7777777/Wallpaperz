from django.core.validators import RegexValidator


name_regex_validator = RegexValidator(
    r'^(?!.*\s{2,})[a-z]+(?: [a-z]+)*$',
    'Ensure that the name contains only lowercase English letters or spaces, with no leading or trailing spaces and no consecutive spaces.'
)
