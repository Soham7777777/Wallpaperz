from typing import Any, cast, override
from django import forms
from app.models import Category, Wallpaper
from project.forms import BootstrapForm
from django.db.models.fields.files import ImageFieldFile


class WallpaperDescriptionModelForm(BootstrapForm, forms.ModelForm[Wallpaper]):

    class Meta:
        model = Wallpaper
        fields = ['description']
        labels = {
            'description': ''
        }
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Write description under 512 characters...',
            }),
        }
    

class WallpaperCategoryModelForm(BootstrapForm, forms.ModelForm[Wallpaper]):

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


class CategoryNameModelForm(BootstrapForm, forms.ModelForm[Category]):

    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Category name here...',
            }),
        }


class CategoryThumbnailModelForm(BootstrapForm, forms.ModelForm[Category]):

    class Meta:
        model = Category
        fields = ['thumbnail']
        labels = {
            'thumbnail': ''
        }
        widgets = {
            'thumbnail': forms.FileInput()
        }


class CategoryThumbnailDeleteModelForm(BootstrapForm, forms.ModelForm[Category]):

    delete_thumbnail = forms.BooleanField(required=True)


    class Meta:
        model = Category
        fields: list[str] = []


    @override
    def save(self, commit: bool = True) -> Category:
        delete_thumbnail = cast(bool, self.cleaned_data['delete_thumbnail'])

        if delete_thumbnail:
            thumbnail_field = cast(ImageFieldFile, self.instance.thumbnail)
            thumbnail_field.delete(save=False)
        
        return super().save(commit)
