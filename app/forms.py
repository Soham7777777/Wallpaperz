from typing import Any, cast, override
from django import forms
from app.models import Category, Wallpaper
from django.db.models.fields.files import ImageFieldFile
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError


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


class CategoryThumbnailModelForm(forms.ModelForm[Category]):
    template_name = 'components/forms/form.html'

    thumbnail = forms.ImageField(label='', required=True, widget=forms.FileInput(attrs={'class': 'form-control'}))


    def clean_thumbnail(self) -> UploadedFile:
        uploaded_file = cast(UploadedFile, self.cleaned_data['thumbnail'])

        if not uploaded_file.name:
            raise ValidationError("Uploaded file must have a name.")

        return uploaded_file


    @override
    def save(self, commit: bool = True) -> Category:
        uploaded_file = cast(UploadedFile, self.cleaned_data['thumbnail'])

        if uploaded_file.name is None:
            raise ValueError("File name is missing; this should have been caught in clean_thumbnail.")

        thumbnail_field = cast(ImageFieldFile, self.instance.thumbnail)
        thumbnail_field.save(uploaded_file.name, uploaded_file, save=commit)

        return super().save(commit)


    class Meta:
        model = Category
        fields = []
