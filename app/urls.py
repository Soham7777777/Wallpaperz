from django.urls import path, reverse_lazy
from django.views.generic import ListView, DetailView
from app.models import Category, Wallpaper
from app.views import FilteredWallpaperListView, HomePageView, CustomHTMXDeleteView


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
        '<slug:slug>',
        DetailView.as_view(
            model=Category,
            template_name='pages/category/page.html',
            context_object_name='category',
        ),
        name='category'
    ),

    path(
        'wallpaper/<slug:slug>',
        DetailView.as_view(
            model=Wallpaper,
            template_name='pages/wallpaper/page.html',
            context_object_name='wallpaper',
        ),
        name='wallpaper'
    ),

    path(
        'delete-category/<slug:slug>',
        CustomHTMXDeleteView.as_view(
            model=Category,
            success_url=reverse_lazy('home'),
            template_name='pages/category/ajax/category_confirm_delete.html',
            context_object_name='category',
        ),
        name='delete_category'
    ),

    path(
        'delete-wallpaper/<slug:slug>',
        CustomHTMXDeleteView.as_view(
            model=Wallpaper,
            success_url=reverse_lazy('home'),
            template_name='pages/wallpaper/ajax/wallpaper_confirm_delete.html',
            context_object_name='wallpaper',
        ),
        name='delete_wallpaper'
    ),

]
