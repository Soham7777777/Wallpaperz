from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import PurePath
from typing import ClassVar, Literal, cast
from django.utils.deconstruct import deconstructible
from django.db.models.fields.files import FieldFile, ImageFieldFile
from django.core.exceptions import ValidationError
from common.image_utils import ImageFormat, get_file_extensions_for_image_format
from PIL import Image
from django.core.files.images import ImageFile


@deconstructible
@dataclass
class MaxFileSizeValidator:

    max_file_size: int

    _max_file_size_range: ClassVar[tuple[Literal[1], Literal[700_000000]]] = 1, 700_000000


    def __post_init__(self) -> None:
        min_size, max_size = MaxFileSizeValidator._max_file_size_range
        if self.max_file_size < min_size or self.max_file_size > max_size:
            raise ValueError(f'The max_file_size ({self.max_file_size}) must be an integer value within {min_size} to {max_size}.')
        

    def __call__(self, value: FieldFile) -> None:
        if value.size > self.max_file_size:
            raise ValidationError(
                'Ensure that the file size is less than or equal to %(max_size)s bytes.',
                code='file_too_large',
                params={'max_size': str(self.max_file_size)},
            )


@deconstructible
@dataclass
class ImageFormatAndFileExtensionsValidator:

    image_formats: Sequence[ImageFormat]


    def __call__(self, value: ImageFieldFile) -> None:
        image_file = cast(ImageFile, value.file)
        with Image.open(image_file) as img:
            image_format = str(img.format)
        
        if image_format not in self.image_formats:
            raise ValidationError(
                'Ensure the image file is in a supported format such as %(formats)s.',
                code='invalid_image_file_format',
                params={'formats': str(tuple([str(format) for format in self.image_formats]))}
            )

        extensions = get_file_extensions_for_image_format(ImageFormat[image_format])
        if PurePath(value.path).suffix not in extensions:
            raise ValidationError(
                'Ensure the image file has a valid extension(e.g. %(extensions)s) corresponding to its format: %(format)s.',
                code='mismatch_between_image_file_extension_and_format',
                params={'extensions': str(extensions), 'format': image_format}
            )


@deconstructible
@dataclass
class ImageDimensionValidator:

    min_width: int | None = None
    min_height: int | None = None
    max_width: int | None = None
    max_height: int | None = None
    

    def __call__(self, value: ImageFieldFile) -> None:
        image_width, image_height = value.width, value.height

        if self.min_width:
            if image_width < self.min_width:
                raise ValidationError(
                    'Ensure the image has minimum width of %(min_width)s pixels.',
                    code='invalid_image_dimension',
                    params={'min_width': self.min_width}
                )
        
        if self.min_height:
            if image_height < self.min_height:
                raise ValidationError(
                    'Ensure the image has minimum height of %(min_height)s pixels.',
                    code='invalid_image_dimension',
                    params={'min_height': self.min_height}
                )
        
        if self.max_width:
            if image_width > self.max_width:
                raise ValidationError(
                    'Ensure the image has maximum width of %(max_width)s pixels.',
                    code='invalid_image_dimension',
                    params={'max_width': self.max_width}
                )
        
        if self.max_height:
            if image_height > self.max_height:
                raise ValidationError(
                    'Ensure the image has maximum height of %(max_height)s pixels.',
                    code='invalid_image_dimension',
                    params={'max_height': self.max_height}
                )
