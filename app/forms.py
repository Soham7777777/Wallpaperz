from typing import Any, cast, override
from django import forms
from django.forms import ValidationError
from app.models import Category, Wallpaper
from project import settings
from project.forms import BootstrapForm, UniqueEmailField
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UsernameField
from django.core.files.uploadedfile import UploadedFile
from django.core.files.images import ImageFile
from common.image_utils import generate_webp_from_jpeg


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


class UserUsernameModelForm(BootstrapForm, forms.ModelForm[User]):

    class Meta:
        model = User
        fields = ['username']
        field_classes = {
            'username': UsernameField
        }


class UserEmailModelForm(BootstrapForm, forms.ModelForm[User]):
    email = UniqueEmailField()

    class Meta:
        model = User
        fields = ['email']


    @override
    def save(self, commit: bool = True) -> User:
        user = super().save(commit)
        user.groups.remove(Group.objects.get(name=settings.VERIFIED_GROUP_NAME))
        return user


class UserFirstNameModelForm(BootstrapForm, forms.ModelForm[User]):

    class Meta:
        model = User
        fields = ['first_name']


class UserLastNameModelForm(BootstrapForm, forms.ModelForm[User]):

    class Meta:
        model = User
        fields = ['last_name']



class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault('widget', MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)
    
    
    @override
    def clean(self, data: list[UploadedFile], initial: list[ImageFile] | None = None) -> list[UploadedFile]:
        single_file_clean = super().clean
        result = [single_file_clean(d, initial) for d in data]
        return result


class WallpapersUploadModelForm(BootstrapForm, forms.ModelForm[Category]):

    wallpapers = MultipleImageField(
        label='Add wallpapers',
        required=False,
        help_text='You may upload up to 3 wallpapers at a time, each in JPEG format (.jpg, .jpeg), at least 1024x1024 pixels in size, and no larger than 7 MB.',
    )


    def clean_wallpapers(self) -> list[Wallpaper]:
        uploaded_wallpapers = cast(list[UploadedFile], self.cleaned_data['wallpapers'])
        if len(uploaded_wallpapers) > settings.MAX_WALLPAPERS_UPLOAD:
            raise ValidationError('You can only upload up to 3 wallpapers at a time.')

        wallpapers = []
        for uploaded_wallpaper in uploaded_wallpapers:
            w = Wallpaper(
                image = uploaded_wallpaper,
                category = self.instance
            )

            try:
                w.full_clean()
            except ValidationError as e:
                raise ValidationError(
                    [f"{uploaded_wallpaper.name}: {msg}" for msgs in e.message_dict.values() for msg in msgs]
                )
            
            wallpapers.append(w)

        return wallpapers


    @override
    def save(self, commit: bool = True) -> Category:
        instance = super().save(commit=commit)

        uploaded_wallpapers = cast(list[Wallpaper], self.cleaned_data['wallpapers'])

        if self.is_valid():
            for uploaded_wallpaper in uploaded_wallpapers:
                uploaded_wallpaper.save()
                compressed_field = cast(ImageFieldFile, uploaded_wallpaper.compressed)
                compressed_field.save('any.webp', generate_webp_from_jpeg(uploaded_wallpaper.image))

        return instance


    class Meta:
        model = Category
        fields: list[str] = []
