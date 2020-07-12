from django.contrib import admin

from .models import (
    MeasuresUpdate,
    PhotosUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate
)


class ProfilePictureUpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'created_at')
    list_display_links = ('id',)
    list_filter = ('created_at', 'accept', 'decline')
    date_hierarchy = 'created_at'
    list_per_page = 24


class CoverPictureUpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'created_at')
    list_display_links = ('id',)
    list_filter = ('created_at', 'accept', 'decline')
    date_hierarchy = 'created_at'
    list_per_page = 24


class MeasuresUpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'measure')
    list_display_links = ('id', 'measure')
    list_filter = ('created_at', 'accept', 'decline')
    date_hierarchy = 'created_at'
    search_fields = ('measure__user__email',)
    list_per_page = 24


class PhotosUpdateAdmin(admin.ModelAdmin):
    readonly_fields = ['related_photo']
    list_display = ['id', 'model']
    list_display_links = ['id']
    list_filter = ['created_at', 'accept', 'decline']
    date_hierarchy = 'created_at'
    list_per_page = 24


admin.site.register(ProfilePictureUpdate, ProfilePictureUpdateAdmin)
admin.site.register(CoverPictureUpdate, CoverPictureUpdateAdmin)
admin.site.register(MeasuresUpdate, MeasuresUpdateAdmin)
admin.site.register(PhotosUpdate, PhotosUpdateAdmin)
