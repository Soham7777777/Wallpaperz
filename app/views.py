from typing import Any
from app.models import Wallpaper, Category
from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView


class FilteredWallpaperListView(ListView[Wallpaper]):

    model = Wallpaper
    template_name = 'app/home/ajax/wallpapers.html'
    paginate_by = 9


    def get_queryset(self) -> QuerySet[Wallpaper, Wallpaper]:
        queryset: QuerySet[Wallpaper, Wallpaper] = super().get_queryset()
        category_name = self.request.GET.get('category')
        if category_name:
            queryset = queryset.filter(category__name__iexact=category_name)
        return queryset


class HomePageView(TemplateView):

    template_name='app/home/page.html'

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values_list('name', flat=True)
        return context
