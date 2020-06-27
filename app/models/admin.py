from django.contrib import admin

from .models import (
    Model,
    ProfilePicture,
    CoverPicture,
    History,
    Mensuration,
    Photo,
    Contact
)


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'city', 'cin', 'user')
    list_display_links = ('id', 'first_name')
    list_per_page = 24


class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'image', 'createdAt')
    list_display_links = ('id',)
    list_filter = ('inUse',)
    list_per_page = 324


class CoverPictureAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'image', 'createdAt')
    list_display_links = ('id',)
    list_filter = ('inUse',)
    list_per_page = 32


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id',)
    list_per_page = 24


class MensurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'taille', 'cheveux', 'permitted', 'user')
    list_display_links = ('id', 'taille', 'permitted')
    list_per_page = 24


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'image')
    list_display_links = ('id',)
    list_filter = ('inUse',)
    list_per_page = 32


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_nom', 'model_email', 'email', 'phone')
    list_display_links = ('id', 'model_nom')
    list_per_page = 24


admin.site.register(Model, ModelAdmin)
admin.site.register(ProfilePicture, ProfilePictureAdmin)
admin.site.register(CoverPicture, CoverPictureAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Mensuration, MensurationAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Contact, ContactAdmin)
