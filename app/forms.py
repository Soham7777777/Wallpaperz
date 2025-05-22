from typing import Any, cast
from django import forms
from app.models import Category, Wallpaper


class WallpaperDescriptionModelForm(forms.ModelForm[Wallpaper]):
    template_name = 'components/forms/form.html'

    class Meta:
        model = Wallpaper
        fields = ['description']
        labels = {
            'description': ''
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Write description under 512 characters...',
                'class': 'form-control'
            }),
        }
    

class WallpaperCategoryModelForm(forms.ModelForm[Wallpaper]):
    template_name = 'components/forms/form.html'


    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        field = cast(forms.ModelChoiceField[Category], self.fields['category']) 
        field.empty_label = None


    class Meta:
        model = Wallpaper
        fields = ['category']
        labels = {
            'category': ''
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class CategoryNameModelForm(forms.ModelForm[Category]):
    template_name = 'components/forms/form.html'

    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Category name here...',
                'class': 'form-control'
            }),
        }
