from dataclasses import dataclass
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.apps.registry import Apps
from common.signals import DeleteAssociatedFilesOnModelDelete
from common.models import AbstractBaseModel


@dataclass
class DeleteHistoricalModelData:

    app_name: str
    model_name: str
    post_delete_file_fields: tuple[str, ...]


    def __call__(self, apps: Apps, schema_editor: BaseDatabaseSchemaEditor) -> None:
        Model = apps.get_model(self.app_name, self.model_name)
        handler = DeleteAssociatedFilesOnModelDelete[AbstractBaseModel](self.post_delete_file_fields)
        for obj in Model.objects.all():
            obj.delete()
            handler(Model, instance=obj)
