from django.conf import settings
from django.urls import path, reverse_lazy
from django.views.generic import ListView, DetailView
from app.views import FilteredWallpaperListView, HomePageView, CustomHTMXDeleteView, ModelEditView, CategoryCreateView, FilteredWallpaperDetailView, download_wallpaper
from app.models import Wallpaper, Category
from django.contrib.auth.decorators import permission_required, login_required
from app import forms
from django.contrib.auth.models import User


verified_group_permissions: list[str] = settings.VERIFIED_GROUP_PERMISIONS
wallpaper_editor_permissions: list[str] = settings.WALLPAPER_EDITOR_PERMISIONS
category_editor_permissions: list[str] = settings.CATEGORY_EDITOR_PERMISIONS

wallpaper_editor_permissions += verified_group_permissions
category_editor_permissions += verified_group_permissions


urlpatterns = [

    path(
        '', 
        HomePageView.as_view(),
        name='home'
    ),

    path(
        'wallpapers',
        FilteredWallpaperListView.as_view(), 
        name='wallpapers'
    ),

    path(
        'categories', 
        ListView.as_view(
            model=Category,
            template_name='pages/categories/page.html',
            context_object_name='categories'
        ), 
        name='categories'
    ),

    path(
        'categories/<slug:slug>',
        DetailView.as_view(
            model=Category,
            template_name='pages/category/page.html',
            context_object_name='category',
        ),
        name='category'
    ),

    path(
        'wallpapers/<slug:slug>',
        FilteredWallpaperDetailView.as_view(),
        name='wallpaper'
    ),

    path(
        'categories/<slug:slug>/delete',
        permission_required([
            *category_editor_permissions
        ])(
            CustomHTMXDeleteView.as_view(
                model=Category,
                success_url=reverse_lazy('home'),
                template_name='pages/category/components/ajax/category_confirm_delete.html',
                context_object_name='category',
            )
        ),
        name='delete_category'
    ),

    path(
        'wallpapers/<slug:slug>/delete',
        permission_required([
            *wallpaper_editor_permissions
        ])(
            CustomHTMXDeleteView.as_view(
                model=Wallpaper,
                success_url=reverse_lazy('home'),
                template_name='pages/wallpaper/components/ajax/wallpaper_confirm_delete.html',
                context_object_name='wallpaper',
            )
        ),
        name='delete_wallpaper'
    ),

    path(
        'wallpapers/<slug:slug>/edit',
        permission_required([
            *wallpaper_editor_permissions
        ])(
            ModelEditView.as_view(
                model=Wallpaper,
                context_instance_name='wallpaper',
                patch_template_name='pages/wallpaper/page.html',
                success_message='Wallpaper updated sucessfully',
                query_to_form_map={
                    'description': (forms.WallpaperDescriptionModelForm, 'pages/wallpaper/components/ajax/description_editing_form.html'),
                    'category': (forms.WallpaperCategoryModelForm, 'pages/wallpaper/components/ajax/category_editing_form.html'),
                }
            )
        ),
        name='edit_wallpaper'
    ),

    path(
        'categories/<slug:slug>/edit',
        permission_required([
            *category_editor_permissions
        ])(
            ModelEditView.as_view(
                model=Category,
                context_instance_name='category',
                patch_template_name='pages/category/page.html',
                success_message='Category updated sucessfully',
                query_to_form_map={
                    'name': (forms.CategoryNameModelForm, 'pages/category/components/ajax/name_editing_form.html'),
                    'thumbnail': (forms.CategoryThumbnailModelForm, 'pages/category/components/ajax/thumbnail_editing_form.html'),
                    'delete_thumbnail': (forms.CategoryThumbnailDeleteModelForm, 'pages/category/components/ajax/category_thumbnail_confirm_delete.html'),
                    'wallpapers': (forms.WallpapersUploadModelForm, 'pages/category/components/ajax/add_wallpapers_form.html'),
                }
            )
        ),
        name='edit_category'
    ),

    path(
        'category/create',
        permission_required([
            *category_editor_permissions
        ])(CategoryCreateView.as_view()),
        name='create_category'
    ),

    path(
        'accounts/<int:slug>/edit',
        login_required(
            ModelEditView.as_view(
                model=User,
                slug_field='id',
                context_instance_name='user',
                patch_template_name='pages/profile/page.html',
                success_message='Account updated sucessfully',
                query_to_form_map={
                    'username': (forms.UserUsernameModelForm, 'pages/profile/components/ajax/username_editing_form.html'),
                    'email': (forms.UserEmailModelForm, 'pages/profile/components/ajax/email_editing_form.html'),
                    'first_name': (forms.UserFirstNameModelForm, 'pages/profile/components/ajax/first_name_editing_form.html'),
                    'last_name': (forms.UserLastNameModelForm, 'pages/profile/components/ajax/last_name_editing_form.html')
                }
            )
        ),
        name='edit_profile'
    ),

    path(
        'download/wallpaper/<slug:slug>',
        permission_required([
            *verified_group_permissions
        ])(
            download_wallpaper
        ),
        name='download_wallpaper'
    ),
]
