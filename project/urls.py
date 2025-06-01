from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from project.admin import admin_site as admin
from django.contrib.auth import views as auth_views
from project.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.views.generic import TemplateView
from app.views import UserCreationView, email_verification, verify_email
from django.contrib.auth.decorators import login_required


urlpatterns = [

    path('', include('app.urls')),
    
    path('admin', admin.urls),

    path(
        'accounts/profile/', 
        login_required(
            TemplateView.as_view(
                template_name='pages/profile/page.html'
            )
        ),
        name='profile'
    ),

    path(
        'accounts/login/',
        auth_views.LoginView.as_view(
            authentication_form=AuthenticationForm
        ),
        name='login'
    ),

    path(
        'accounts/logout/', 
        login_required(auth_views.LogoutView.as_view()),
        name='logout'
    ),

    path(
        'accounts/password_reset/',
        auth_views.PasswordResetView.as_view(
            form_class=PasswordResetForm
        ),
        name='password_reset'
    ),
    
    path(
        'accounts/password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    path(
        'accounts/reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            form_class=SetPasswordForm,
        ),
        name='password_reset_confirm'
    ),

    path(
        'accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    path(
        'accounts/password_change/',
        login_required(
            auth_views.PasswordChangeView.as_view(
                form_class=PasswordChangeForm
            )
        ),
        name='password_change'
    ),

    path(
        'accounts/password_change/done/',
        login_required(auth_views.PasswordChangeDoneView.as_view()),
        name='password_change_done'
    ),

    path(
        'accounts/create_user/',
        UserCreationView.as_view(),
        name='create_user'
    ),

    path(
        'accounts/email_verification/',
        login_required(email_verification),
        name='email_verification'
    ),

    path(
        'accounts/verify_email/<uidb64>/<token>/',
        verify_email,
        name='verify_email'
    ),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
