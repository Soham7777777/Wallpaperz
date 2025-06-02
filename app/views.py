from typing import Any, TypeAlias, override
from django.conf import settings
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.forms import ModelForm, ValidationError
from django.urls import reverse
from app.models import Wallpaper, Category
from django.db.models.query import QuerySet
from django.views.generic import ListView, TemplateView, DeleteView, View, DetailView
from typing import cast
from django.db import models
from common.models import AbstractBaseModel
from django.contrib import messages
from app.forms import CategoryNameModelForm
from project.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, Group
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache


_User: TypeAlias = AbstractBaseUser
UserModel = get_user_model()



class FilteredWallpaperListView(ListView[Wallpaper]):

    model = Wallpaper
    template_name = 'components/ajax/wallpapers.html'
    paginate_by = settings.WALLPAPER_PEGINATION_PER_PAGE


    @override
    def get_queryset(self) -> QuerySet[Wallpaper, Wallpaper]:
        queryset: QuerySet[Wallpaper, Wallpaper] = super().get_queryset()

        queryset = queryset.exclude(compressed='')

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


class CustomHTMXDeleteView(DeleteView[AbstractBaseModel, ModelForm[AbstractBaseModel]]):

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


class ModelEditView(View):
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
        if obj is None:
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


    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form_class, form_template = self.get_form(request)
        instance = self.get_object()
        form = form_class(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.success(request, self.success_message)
            context = self.get_context_data(oob_swap_messages=True)
            return render(request, self.patch_template_name, context)
        
        context = self.get_context_data(form=form)
        return render(request, form_template, context)


class CategoryCreateView(View):

    form_class = CategoryNameModelForm
    template_name = 'pages/categories/components/ajax/category_creation_form.html'


    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, dict(form=form))


    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Category created successfully.')
            return render(request, 'pages/categories/components/ajax/category_card.html', dict(category=category))
        return render(request, self.template_name, dict(form=form))


class UserCreationView(View):

    form_class = UserCreationForm
    template_name = 'registration/create_user.html'


    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class()
        return render(request, self.template_name, dict(form=form))
    

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Account created successfully.')
            response = HttpResponse()
            response.headers['HX-Location'] = reverse('login')
            response.status_code = 204
            return response
        return render(request, self.template_name, dict(form=form))


def email_verification(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        opts = {
            'use_https': request.is_secure(),
            'token_generator': default_token_generator,
            'from_email': None,
            'email_template_name': 'registration/email_verification_email.html',
            'subject_template_name': 'registration/email_verification_subject.txt',
            'request': request,
            'html_email_template_name': None,
            'extra_email_context': None,
        }
        form = PasswordResetForm(dict(email=request.user.email))
        if form.is_valid():
            form.save(**opts)
        else:
            raise Http404()
        return render(request, 'registration/email_verification_done.html')
    raise Http404()


@sensitive_post_parameters()
@never_cache
def verify_email(request: HttpRequest, uidb64: str, token: str) -> HttpResponse:
    # code taken from PasswordResetConfirmView

    internal_email_verification_session = '_email_verification_token'
    email_verification_url = 'verify-email'

    def get_user(uidb64: str) -> _User | None:
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            pk = UserModel._meta.pk.to_python(uid)
            user = UserModel._default_manager.get(pk=pk)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    user = get_user(uidb64)

    if user is not None:
        token = token
        if token == email_verification_url:
            session_token = request.session.get(internal_email_verification_session)
            if default_token_generator.check_token(user, session_token):
                user = cast(User, user)
                user.groups.add(Group.objects.get(name=settings.VERIFIED_GROUP_NAME))
                messages.success(request, 'Email verified successfully.')

                if request.user.is_authenticated:
                    return HttpResponseRedirect(reverse('profile'))
                else:
                    return HttpResponseRedirect(reverse('login'))
        else:
            if default_token_generator.check_token(user, token):
                # Store the token in the session and redirect to the
                # email verification URL without the token. That
                # avoids the possibility of leaking the token in the
                # HTTP Referer header.
                request.session[internal_email_verification_session] = token
                redirect_url = request.path.replace(
                    token, email_verification_url
                )
                return HttpResponseRedirect(redirect_url)
            
    raise Http404()


class FilteredWallpaperDetailView(DetailView[Wallpaper]):
    model = Wallpaper
    template_name = 'pages/wallpaper/page.html'
    context_object_name = 'wallpaper'


    @override
    def get_queryset(self) -> QuerySet[Wallpaper, Wallpaper]:
        return super().get_queryset().exclude(compressed='')
