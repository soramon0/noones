from django.contrib import admin

from .models import MeasuresUpdate, PhotosUpdate, ProfilePictureUpdate


class ProfilePictureUpdateAdmin(admin.ModelAdmin):
    list_display = ['id', 'model', 'timestamp']
    list_display_links = ['id']
    list_filter = ['timestamp', 'accept', 'decline']
    date_hierarchy = 'timestamp'
    list_per_page = 24


class MeasuresUpdateAdmin(admin.ModelAdmin):
    list_display = ('id', 'measure', 'timestamp')
    list_display_links = ('id', 'measure')
    list_filter = ['timestamp']
    date_hierarchy = 'timestamp'
    search_fields = ['measure__user__email']
    list_per_page = 24


class PhotosUpdateAdmin(admin.ModelAdmin):
    readonly_fields = ['related_photo']
    list_display = ['id', 'model', 'timestamp']
    list_display_links = ['id']
    list_filter = ['timestamp', 'accept', 'decline']
    date_hierarchy = 'timestamp'
    list_per_page = 24


admin.site.register(ProfilePictureUpdate, ProfilePictureUpdateAdmin)
admin.site.register(MeasuresUpdate, MeasuresUpdateAdmin)
admin.site.register(PhotosUpdate, PhotosUpdateAdmin)
