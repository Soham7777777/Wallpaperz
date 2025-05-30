from django.urls import path, reverse_lazy
from django.views.generic import ListView, DetailView
from app.models import Category, Wallpaper
from app.views import FilteredWallpaperListView, HomePageView, CustomHTMXDeleteView, ModelEditView, CategoryCreateView
from app import forms


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
        DetailView.as_view(
            model=Wallpaper,
            template_name='pages/wallpaper/page.html',
            context_object_name='wallpaper',
        ),
        name='wallpaper'
    ),

    path(
        'categories/<slug:slug>/delete',
        CustomHTMXDeleteView.as_view(
            model=Category,
            success_url=reverse_lazy('home'),
            template_name='pages/category/components/ajax/category_confirm_delete.html',
            context_object_name='category',
        ),
        name='delete_category'
    ),

    path(
        'wallpapers/<slug:slug>/delete',
        CustomHTMXDeleteView.as_view(
            model=Wallpaper,
            success_url=reverse_lazy('home'),
            template_name='pages/wallpaper/components/ajax/wallpaper_confirm_delete.html',
            context_object_name='wallpaper',
        ),
        name='delete_wallpaper'
    ),

    path(
        'wallpapers/<slug:slug>/edit',
        ModelEditView.as_view(
            model=Wallpaper,
            context_instance_name='wallpaper',
            patch_template_name='pages/wallpaper/page.html',
            success_message='Wallpaper updated sucessfully',
            query_to_form_map={
                'description': (forms.WallpaperDescriptionModelForm, 'pages/wallpaper/components/ajax/description_editing_form.html'),
                'category': (forms.WallpaperCategoryModelForm, 'pages/wallpaper/components/ajax/category_editing_form.html')
            }
        ),
        name='edit_wallpaper'
    ),

    path(
        'categories/<slug:slug>/edit',
        ModelEditView.as_view(
            model=Category,
            context_instance_name='category',
            patch_template_name='pages/category/page.html',
            success_message='Category updated sucessfully',
            query_to_form_map={
                'name': (forms.CategoryNameModelForm, 'pages/category/components/ajax/name_editing_form.html'),
                'thumbnail': (forms.CategoryThumbnailModelForm, 'pages/category/components/ajax/thumbnail_editing_form.html'),
                'delete_thumbnail': (forms.CategoryThumbnailDeleteModelForm, 'pages/category/components/ajax/category_thumbnail_confirm_delete.html')
            }
        ),
        name='edit_category'
    ),

    path(
        'category/create',
        CategoryCreateView.as_view(),
        name='create_category'
    ),

]
