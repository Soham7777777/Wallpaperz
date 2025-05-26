from django.forms.renderers import TemplatesSetting


class BootstrapFormRendered(TemplatesSetting):
    form_template_name = 'components/forms/layout.html'
    field_template_name = 'components/forms/field.html'
