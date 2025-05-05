from typing import override
from django.db import models
from pathlib import PurePath
from common.models import AbstractBaseModel
from common.image_utils import ImageFormat
from common.validators import ImageFormatAndFileExtensionsValidator, MaxFileSizeValidator, ImageDimensionValidator
from common.unique_file_path_generators import UniqueFilePathGenerator
from common.constants import MB
from common import regexes
from django.core import validators
from django_stubs_ext.db.models.manager import RelatedManager
from django.utils.text import slugify
from django.core import validators


class Wallpaper(AbstractBaseModel):
    image = models.ImageField(
        unique=True,
        upload_to=UniqueFilePathGenerator(
            PurePath('wallpapers/'),
            'image'
        ),
        validators=[
            MaxFileSizeValidator(7 * MB),
            ImageFormatAndFileExtensionsValidator((ImageFormat.JPEG, )),
            ImageDimensionValidator(
                min_width=1024,
                min_height=1024,
            )
        ],
        max_length=256
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='wallpapers',
    )
    slug = models.SlugField(
        max_length=32,
        validators=[
            validators.MinLengthValidator(32),
            regexes.uuid_regex_validator,
        ]
    )

    objects: models.Manager['Wallpaper'] = models.Manager()


    @override
    def clean(self) -> None:
        self.slug = self.uuid.hex


class Category(AbstractBaseModel):
    name = models.CharField(
        unique=True,
        max_length=32,
        validators=[
            validators.MinLengthValidator(2),
            regexes.name_regex_validator,
        ],
    )
    thumbnail = models.ImageField(
        null=True,
        upload_to=UniqueFilePathGenerator(
            PurePath('category-thumbnails/'),
            'image'
        ),
        validators=[
            MaxFileSizeValidator(1 * MB),
            ImageFormatAndFileExtensionsValidator(
                (ImageFormat.JPEG, ImageFormat.PNG, ImageFormat.WEBP)
            ),
            ImageDimensionValidator(
                min_width=512,
                min_height=512,
            )
        ],
        max_length=256
    )
    slug = models.SlugField(
        max_length=32
    )

    wallpapers: RelatedManager[Wallpaper]

    objects: models.Manager['Category'] = models.Manager()


    @override
    def clean(self) -> None:
        self.slug = slugify(self.name)
