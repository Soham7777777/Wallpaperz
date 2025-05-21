from typing import override
from django import forms
from app.models import Wallpaper


class WallpaperDescriptionModelForm(forms.ModelForm[Wallpaper]):
    template_name = 'components/ajax/form.html'

    class Meta:
        model = Wallpaper
        fields = ['description']
        labels = {
            'description': ''
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Write description under 512 characters...'}),
        }
