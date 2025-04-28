from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, cast
from django.db import models
from django.db.models.fields.files import FieldFile
from common.models import AbstractBaseModel
from django.core.exceptions import ObjectDoesNotExist


@dataclass(frozen=True)
class AbstractModelSignalHandler[T: AbstractBaseModel](ABC):

    @abstractmethod
    def __call__(self, sender: type[T], **kwargs: Any) -> None: ...


@dataclass(frozen=True)
class DeleteAssociatedFilesOnModelDelete[T: AbstractBaseModel](AbstractModelSignalHandler[T]):

    target_file_fields: tuple[str, ...]


    def __call__(self, sender: type[T], **kwargs: Any) -> None:
        instance = cast(T, kwargs['instance'])

        for field in instance._meta.get_fields():
            if isinstance(field, models.FileField) and ((file_field_name:=field.get_attname()) in self.target_file_fields):
                file = cast(FieldFile, getattr(instance, file_field_name))
                file.delete(save=False)


@dataclass(frozen=True)
class DeleteAssociatedOldFilesOnModelUpdate[T: AbstractBaseModel](AbstractModelSignalHandler[T]):

    target_file_fields: tuple[str, ...]


    def __call__(self, sender: type[T], **kwargs: Any) -> None:
        instance = cast(T, kwargs['instance'])

        for field in instance._meta.get_fields():
            if isinstance(field, models.FileField) and ((file_field_name:=field.get_attname()) in self.target_file_fields):
                current_file = cast(FieldFile, getattr(instance, file_field_name))
                try:
                    old_file = cast(FieldFile, getattr(sender.objects.get(pk=instance.pk), file_field_name))
                except ObjectDoesNotExist:
                    return
                if current_file.name != old_file.name:
                    old_file.delete(save=False)
