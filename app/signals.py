from typing import Any
from django.apps.config import AppConfig
from django.apps.registry import Apps
from django.contrib.auth.management import create_permissions
from django.db import DEFAULT_DB_ALIAS
from django.apps import apps as global_apps
from django.conf import settings


def connect_permissions_with_groups(    
    app_config: AppConfig,
    verbosity: int = 2,
    interactive: bool = True,
    using: str = DEFAULT_DB_ALIAS,
    apps: Apps = global_apps,
    **kwargs: Any,
) -> None:


    # code taken from create_permissions at django/contrib/auth/management/__init__.py

    try:
        Permission = apps.get_model('auth', 'Permission')
        Group = apps.get_model('auth', 'Group')
        ContentType = apps.get_model('contenttypes', 'ContentType')
        Wallpaper = apps.get_model(app_config.label, 'Wallpaper')
    except LookupError:
        return

    # Ensure that permissions are created for this app. Needed if
    # 'app' is in INSTALLED_APPS before
    # 'django.contrib.auth'.
    create_permissions(
        app_config,
        verbosity=verbosity,
        interactive=interactive,
        using=using,
        apps=apps,
        **kwargs,
    )

    # idempotent implementation

    # for verified group
    verified_group = Group.objects.get(name=settings.VERIFIED_GROUP_NAME)
    verified_group_permissions_to_apply: list[str] = settings.VERIFIED_GROUP_PERMISIONS
    content_type = ContentType.objects.get_for_model(Wallpaper)

    for permission_codename in verified_group_permissions_to_apply:
        codename = permission_codename.split('.')[-1]

        existing_permission = Permission.objects.filter(codename=codename, content_type=content_type).first()

        if existing_permission is None:        
            name = ' '.join(codename.split('_')).title()
            verified_group.permissions.add(
                Permission.objects.create(
                    name=name,
                    codename=codename,
                    content_type=content_type
                )
            )
            if verbosity >= 2:
                print(f'Connected permission {codename} with "Verified" Group')

    # for category editor group
    category_editor_group = Group.objects.get(name=settings.CATEGORY_EDITOR_GROUP_NAME)
    category_editor_group_applied_permission_codenames = category_editor_group.permissions.all().values_list('codename', flat=True)

    category_editor_group_permissions_to_apply: list[str] = settings.CATEGORY_EDITOR_PERMISIONS
    for permission_codename in category_editor_group_permissions_to_apply:
        codename = permission_codename.split('.')[-1]
        if codename not in category_editor_group_applied_permission_codenames:
            category_editor_group.permissions.add(
                Permission.objects.filter(codename=codename).first()
            )
            if verbosity >= 2:
                print(f'Connected permission {codename} with "Category Editor" Group')
    
    # for wallpaper editor group
    wallpaper_editor_group = Group.objects.get(name=settings.WALLPAPER_EDITOR_GROUP_NAME)
    wallpaper_editor_group_applied_permission_codenames = wallpaper_editor_group.permissions.all().values_list('codename', flat=True)

    wallpaper_editor_group_permissions_to_apply: list[str] = settings.WALLPAPER_EDITOR_PERMISIONS
    for permission_codename in wallpaper_editor_group_permissions_to_apply:
        codename = permission_codename.split('.')[-1]
        if codename not in wallpaper_editor_group_applied_permission_codenames:
            wallpaper_editor_group.permissions.add(
                Permission.objects.filter(codename=codename).first()
            )
            if verbosity >= 2:
                print(f'Connected permission {codename} with "Wallpaper Editor" Group')
