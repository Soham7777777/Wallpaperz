from django.contrib import admin
from django.contrib.auth.models import Group, User


class WallpaperzAdminSite(admin.AdminSite):
    site_header = 'Wallpaperz administration'


admin_site = WallpaperzAdminSite(name='wallpaperzadmin')
admin_site.register(User)
admin_site.register(Group)
