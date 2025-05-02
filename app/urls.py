from django.urls import path
from django.views.generic import TemplateView, ListView
from app.models import Wallpaper, Category


urlpatterns = [

    path(
        '', 
        TemplateView.as_view(
            template_name='app/home/page.html'
        ), 
        name='home'
    ),

    path(
        'wallpapers',
        ListView.as_view(
            model=Wallpaper,
            paginate_by=9, 
            template_name='app/home/ajax/wallpapers.html'
        ), 
        name='wallpapers'
    ),

    path(
        'categories', 
        ListView.as_view(
            model=Category,
            template_name='app/categories/page.html',
            context_object_name='categories'
        ), 
        name='categories'
    ),

]
