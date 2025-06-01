from django import template
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.conf import settings


register = template.Library()


verified_group_name = settings.VERIFIED_GROUP_NAME
category_editor_group_name = settings.CATEGORY_EDITOR_GROUP_NAME
wallpaper_editor_group_name = settings.WALLPAPER_EDITOR_GROUP_NAME


@register.filter(name='get_roles')
def get_roles(user: User) -> QuerySet[Group, Group]:
    return user.groups.exclude(name=verified_group_name)


@register.filter(name='is_verified')
def is_verified(user: User) -> bool:
    return user.is_authenticated and user.groups.filter(name=verified_group_name).exists()


@register.filter(name='is_category_editor')
def is_category_editor(user: User) -> bool:
    return user.is_authenticated and user.groups.filter(name=category_editor_group_name).exists()


@register.filter(name='is_wallpaper_editor')
def is_wallpaper_editor(user: User) -> bool:
    return user.is_authenticated and user.groups.filter(name=wallpaper_editor_group_name).exists()