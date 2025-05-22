from typing import Any, override
from django.http import HttpRequest, HttpResponse, Http404, QueryDict
from django.shortcuts import render
from django.forms import ModelForm
from app.models import Wallpaper, Category
from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView, DeleteView, View
from typing import cast
from django.db import models
from common.models import AbstractBaseModel
from django.forms.models import BaseModelForm
from django.contrib import messages


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


class ModelPatchView(View):
    model: type[AbstractBaseModel] | None = None
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_instance_name = ''
    success_message = ''
    extra_context: dict[str, Any] | None = None
    patch_template_name = ''
    query_to_form_map: dict[str, tuple[type[ModelForm[AbstractBaseModel]], str]] = {}


    def get_object(self) -> AbstractBaseModel:
        if self.model is None:
            raise AttributeError('"model" argument is required for this class based view.')
        
        slug = self.kwargs.get(self.slug_url_kwarg)
        obj = self.model.objects.filter(**{self.slug_field: slug}).first()
        if not obj:
            raise Http404(f'{self.model.__name__} with {self.slug_field}={slug} not found')

        return obj


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = {
            **(self.extra_context or {}),
            **kwargs,
        }
        if self.context_instance_name:
            context[self.context_instance_name] = self.get_object()
        else:
            raise AttributeError('"context_instance_name" is required for this class based view')
        return context


    def get_form(self, request: HttpRequest) -> tuple[type[ModelForm[AbstractBaseModel]], str]:
        form_name = request.GET.get('form')

        if not form_name or form_name not in self.query_to_form_map:
            raise Http404('Form type not found.')

        form_class, form_template = self.query_to_form_map[form_name]
        return form_class, form_template


    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form_class, form_template = self.get_form(request)
        instance = self.get_object()
        form = form_class(instance=instance)
        context = self.get_context_data(form=form)
        return render(request, form_template, context)


    def patch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form_class, form_template = self.get_form(request)
        instance = self.get_object()
        patch_data = QueryDict(request.body)
        form = form_class(patch_data, instance=instance)

        if form.is_valid():
            form.save()
            if form.has_changed():
                messages.success(request, self.success_message)
            context = self.get_context_data(oob_swap_messages=True)
            return render(request, self.patch_template_name, context)
        
        context = self.get_context_data(form=form)
        return render(request, form_template, context)
