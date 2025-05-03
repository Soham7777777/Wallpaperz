from django.urls import path
from django.views.generic import ListView, DetailView
from app.models import Category
from app.views import FilteredWallpaperListView, HomePageView


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
            template_name='app/categories.html',
            context_object_name='categories'
        ), 
        name='categories'
    ),

    path(
        '<slug:slug>',
        DetailView.as_view(
            model=Category,
            template_name='app/category.html',
            context_object_name='category',
        ),
        name='category'
    ),

]
