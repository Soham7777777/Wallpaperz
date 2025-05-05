from django.core.validators import RegexValidator


name_regex_validator = RegexValidator(
    r'^(?!.*\s{2,})[a-z]+(?: [a-z]+)*$',
    'Ensure that the name contains only lowercase English letters or spaces, with no leading or trailing spaces and no consecutive spaces.'
)


uuid_regex_validator = RegexValidator(
    r'^[0-9a-f]$',
    'Ensure that the UUID contains only digits and the lowercase English letters \'a\' to \'f\'.'
)
