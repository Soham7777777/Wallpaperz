from django.db import models
from pathlib import PurePath
from common.models import AbstractBaseModel
from common.image_utils import ImageFormat
from common.validators import ImageFormatAndFileExtensionsValidator, MaxFileSizeValidator
from common.unique_file_path_generators import UniqueFilePathGenerator
from common.constants import MB


class Wallpaper(AbstractBaseModel):
    image = models.ImageField(
        unique=True,
        upload_to=UniqueFilePathGenerator(
            PurePath('wallpapers/'),
            'image'
        ),
        validators=[
            MaxFileSizeValidator(7 * MB),
            ImageFormatAndFileExtensionsValidator((ImageFormat.JPEG, ))
        ],
        max_length=256
    )

    objects: models.Manager["Wallpaper"] = models.Manager()
