from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from project.admin import admin_site as admin


urlpatterns = [

    path('', include('app.urls')),
    path('admin', admin.urls)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
