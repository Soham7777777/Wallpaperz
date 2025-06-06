# Generated by Django 5.2 on 2025-04-28 15:15

import common.image_utils
import common.unique_file_path_generators
import common.validators
import pathlib
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallpaper',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(max_length=256, unique=True, upload_to=common.unique_file_path_generators.UniqueFilePathGenerator(pathlib.PurePosixPath('wallpapers'), 'image'), validators=[common.validators.MaxFileSizeValidator(7340032), common.validators.ImageFormatAndFileExtensionsValidator((common.image_utils.ImageFormat['JPEG'],))])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
