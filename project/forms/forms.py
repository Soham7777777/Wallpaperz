from typing import Any, cast
from django import forms


class BootstrapForm(forms.Form):
    template_name_label = 'components/forms/label.html'


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            widget = cast(forms.Widget, field.widget)
            existing_classes = widget.attrs.get('class', '').split()

            if isinstance(widget, (forms.TextInput, forms.Textarea, forms.FileInput)):
                if 'form-control' not in existing_classes:
                    existing_classes.append('form-control')
            elif isinstance(widget, forms.Select):
                if 'form-select' not in existing_classes:
                    existing_classes.append('form-select')

            if self.errors.get(field_name):
                validation_class = 'is-invalid'
            else:
                validation_class = 'is-valid'

            if validation_class not in existing_classes:
                existing_classes.append(validation_class)

            widget.attrs['class'] = ' '.join(existing_classes)