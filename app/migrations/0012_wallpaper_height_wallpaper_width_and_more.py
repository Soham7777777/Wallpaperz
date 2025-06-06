# Generated by Django 5.2 on 2025-05-19 03:45

import common.image_utils
import common.unique_file_path_generators
import common.validators
import pathlib
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_wallpaper_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallpaper',
            name='height',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='wallpaper',
            name='width',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='wallpaper',
            name='image',
            field=models.ImageField(height_field='height', max_length=256, unique=True, upload_to=common.unique_file_path_generators.UniqueFilePathGenerator(pathlib.PurePosixPath('wallpapers'), 'image'), validators=[common.validators.MaxFileSizeValidator(7340032), common.validators.ImageFormatAndFileExtensionsValidator((common.image_utils.ImageFormat['JPEG'],)), common.validators.ImageDimensionValidator(min_height=1024, min_width=1024)], width_field='width'),
        ),
    ]
