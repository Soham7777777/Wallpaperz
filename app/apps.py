from typing import override
from django.apps import AppConfig as ApplicationConfig
from app.signals import connect_permissions_with_groups
from django.db.models.signals import post_delete, pre_save, post_migrate


class AppConfig(ApplicationConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Wallpaperz'


    @override
    def ready(self) -> None:
        from common.signals import DeleteAssociatedFilesOnModelDelete, DeleteAssociatedOldFilesOnModelUpdate
        from app.models import Wallpaper, Category

        post_delete.connect(
            DeleteAssociatedFilesOnModelDelete[Wallpaper](('image', 'compressed')),
            sender=Wallpaper,
            dispatch_uid='WALLPAPER_DELETE_FILES_POST_DELETE'
        )

        pre_save.connect(
            DeleteAssociatedOldFilesOnModelUpdate[Wallpaper](('image', 'compressed')),
            sender=Wallpaper,
            dispatch_uid='WALLPAPER_DELETE_OLD_FILES_PRE_SAVE'
        )


        post_delete.connect(
            DeleteAssociatedFilesOnModelDelete[Category](('thumbnail', )),
            sender=Category,
            dispatch_uid='CATEGORY_DELETE_FILES_POST_DELETE'
        )

        pre_save.connect(
            DeleteAssociatedOldFilesOnModelUpdate[Category](('thumbnail', )),
            sender=Category,
            dispatch_uid='CATEGORY_DELETE_OLD_FILES_PRE_SAVE'
        )

        post_migrate.connect(connect_permissions_with_groups, dispatch_uid='GROUP_PERMISSION_CONNECTION_POST_MIGRATE')
