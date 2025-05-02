from django import forms
from app.models import Category
from functools import partial


class CategorySelectForm(forms.Form):
    category = forms.ChoiceField(
        choices=partial(Category.objects.values_list, 'name', flat=True)
    )