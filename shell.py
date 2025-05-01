import os
import django
import django_stubs_ext

django_stubs_ext.monkeypatch()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

# ==========================================================
# ==========================================================
# ==========================================================
# ==========================================================
# ==========================================================

from app.models import Wallpaper, Category
from django.conf import settings
from pathlib import Path
from django.core.files.images import ImageFile


categories_directory: Path = settings.BASE_DIR / 'images/categories'
wallpapers_directory: Path = settings.BASE_DIR / 'images/wallpapers'


with Path((categories_directory / 'abstract.webp').relative_to(settings.BASE_DIR)).open('rb') as f:
    c1 = Category(name='abstract', thumbnail=ImageFile(f))
    c1.full_clean()
    c1.save()


with Path((categories_directory / 'paradise.webp').relative_to(settings.BASE_DIR)).open('rb') as f:
    c2 = Category(name='abstract', thumbnail=ImageFile(f))
    c2.full_clean()
    c2.save()

Wallpaper.objects.all()
