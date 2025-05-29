from django.contrib import admin
from django.contrib.auth.models import User, Group
from app.models import Wallpaper, Category


class WallpaperzAdminSite(admin.AdminSite):
    site_header = 'Wallpaperz administration'


admin_site = WallpaperzAdminSite(name='wallpaperzadmin')
admin_site.register(User)
admin_site.register(Group)
admin_site.register(Wallpaper)
admin_site.register(Category)
