# Generated by Django 5.2 on 2025-06-02 11:13

from operator import attrgetter
from pathlib import Path
from django.db import migrations
from django.apps.registry import Apps
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.conf import settings
from django.core.files.images import ImageFile
from common.models import AbstractBaseModel
from common.signals import DeleteAssociatedOldFilesOnModelUpdate


compressed_wallpapers_directory: Path = settings.BASE_DIR / 'images/compressed/'


def set_compressed_wallpapers(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Wallpaper = apps.get_model('app', 'Wallpaper')
    compressed_files = sorted(compressed_wallpapers_directory.glob('*'), key=attrgetter('name'))
    wallpapers = Wallpaper.objects.all()

    for wallpaper_obj, compressed_file in zip(wallpapers, compressed_files):
        file = compressed_file.relative_to(settings.BASE_DIR)
        wallpaper_obj.compressed = ImageFile(file.open('rb'))
        wallpaper_obj.save()


def delete_compressed_wallpapers(apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Wallpaper = apps.get_model('app', 'Wallpaper')
    handler = DeleteAssociatedOldFilesOnModelUpdate[AbstractBaseModel](('compressed',))
    for wallpaper_obj in Wallpaper.objects.all():
        wallpaper_obj.compressed = None
        handler(Wallpaper, instance=wallpaper_obj)
        wallpaper_obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_wallpaper_compressed'),
    ]

    operations = [
        migrations.RunPython(
            set_compressed_wallpapers,
            delete_compressed_wallpapers
        )
    ]
