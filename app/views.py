from typing import Any, override
from django.http import HttpRequest, HttpResponse, Http404, QueryDict
from django.shortcuts import render
from app.models import Wallpaper, Category
from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView, DeleteView
from typing import cast
from django.db import models
from common.models import AbstractBaseModel
from django.forms.models import BaseModelForm
from django.contrib import messages
from app.forms import WallpaperDescriptionModelForm


class FilteredWallpaperListView(ListView[Wallpaper]):

    model = Wallpaper
    template_name = 'components/ajax/wallpapers.html'
    paginate_by = 9


    @override
    def get_queryset(self) -> QuerySet[Wallpaper, Wallpaper]:
        queryset: QuerySet[Wallpaper, Wallpaper] = super().get_queryset()

        category_name = self.request.GET.get('category')
        if category_name:
            queryset = queryset.filter(category__slug__iexact=category_name)

        orientation = self.request.GET.get('orientation')
        if orientation:
            match orientation:
                case 'landscape':
                    queryset = queryset.filter(width__gte=models.F('height'))
                case 'portrait':
                    queryset = queryset.filter(width__lte=models.F('height'))

        return queryset


class HomePageView(TemplateView):

    template_name='pages/home/page.html'

    
    @override
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.values('name', 'slug')
        context['has_wallpaper_data'] = Wallpaper.objects.exists()
        return context


class CustomHTMXDeleteView(DeleteView[AbstractBaseModel, BaseModelForm[AbstractBaseModel]]):

    success_message: str | None = None


    def get_success_message(self) -> str:
        if self.success_message:
            return self.success_message

        if isinstance(self.model, type) and issubclass(self.model, models.Model):
            model = cast(models.Model,  self.model)
            return f'{str(model._meta.verbose_name).title()} deleted successfully.'

        return 'Resource deleted successfully.'


    @override
    def delete(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, self.get_success_message())

        response = HttpResponse()
        response['HX-Location'] = self.get_success_url()
        response.status_code = 204

        return response


def edit_wallpaper_description(request: HttpRequest, slug: str) -> HttpResponse:
    wallpaper = Wallpaper.objects.filter(slug=slug).first()

    if wallpaper is not None:
        form = WallpaperDescriptionModelForm(instance=wallpaper)

        if request.method == 'PATCH':
            form = WallpaperDescriptionModelForm(QueryDict(request.body), instance=wallpaper)
            if form.is_valid():
                form.save()
                messages.success(request, 'Description updated sucessfully')
                return render(request, 'pages/wallpaper/page.html', dict(wallpaper=wallpaper, oob_swap_messages=True))
            
        return render(request, 'pages/wallpaper/components/ajax/forms/description_form.html', dict(form=form, wallpaper=wallpaper))

    raise Http404()
