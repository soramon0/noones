from django.contrib import admin

from .models import User, Image, Header


class UserAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_per_page = 25
    list_filter = ('email', 'is_active')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'inUse', 'image')
    list_editable = ('inUse',)
    list_per_page = 25


class HeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'inUse', 'image')
    list_editable = ('inUse',)
    list_per_page = 25


admin.site.register(User, UserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Header, HeaderAdmin)
