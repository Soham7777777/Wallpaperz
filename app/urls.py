from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [

    path('', TemplateView.as_view(template_name='app/home.html'), name='home'),
    path('categories', TemplateView.as_view(template_name='app/categories.html'), name='categories'),

]
