from typing import TYPE_CHECKING, Any, cast
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm as SetPasswordAuthForm
from django.forms import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class BootstrapForm(forms.Form):
    template_name_label = 'components/forms/label.html'


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = cast(forms.Widget, field.widget)
            existing_classes = widget.attrs.get('class', '').split()

            if isinstance(widget, (forms.TextInput, forms.Textarea, forms.FileInput, forms.PasswordInput, forms.EmailInput)):
                if 'form-control' not in existing_classes:
                    existing_classes.append('form-control')
            elif isinstance(widget, forms.Select):
                if 'form-select' not in existing_classes:
                    existing_classes.append('form-select')

            widget.attrs['class'] = ' '.join(existing_classes)


class AuthenticationForm(BootstrapForm, auth_forms.AuthenticationForm):
    pass


class PasswordResetForm(BootstrapForm, auth_forms.PasswordResetForm):
    pass


if TYPE_CHECKING:
    _BaseSetPasswordForm: type[SetPasswordAuthForm[User]] = SetPasswordAuthForm
else:
    _BaseSetPasswordForm = SetPasswordAuthForm


class SetPasswordForm(BootstrapForm, _BaseSetPasswordForm):  # type: ignore[valid-type, misc]
    pass


class PasswordChangeForm(BootstrapForm, auth_forms.PasswordChangeForm):
    pass


def validate_unique_email(value: str) -> None:
    if User.objects.filter(email=value).exists():
        raise ValidationError('A user with that email already exists.', code='duplicate_email')


def UniqueEmailField(**kwargs: Any) -> forms.EmailField:
    return forms.EmailField(
        required=True,
        help_text='Email must be unique across all users.',
        validators=[validate_unique_email],
        **kwargs
    )

class UserCreationForm(BootstrapForm, auth_forms.UserCreationForm[User]):
    email = UniqueEmailField()
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta(auth_forms.UserCreationForm.Meta):  # type: ignore[name-defined, misc]
        fields = ['username', 'email', 'password1', 'password2', 'captcha']