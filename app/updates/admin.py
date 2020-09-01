from django.contrib import admin

from updates.models import (
    ProfileUpdate,
    MeasuresUpdate,
    GalleryUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate,
)
from updates.actions import accept_update


class ProfileUpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at")
    list_display_links = ("id", "user")
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    search_fields = ("user__email",)
    list_per_page = 24
    actions = (accept_update,)


class MeasuresUpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "measures", "created_at")
    list_display_links = ("id", "measures")
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    search_fields = ("user__email",)
    list_per_page = 24
    actions = (accept_update,)


class ProfilePictureUpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "image", "created_at")
    list_display_links = ("id",)
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    list_per_page = 24
    actions = (accept_update,)


class CoverPictureUpdateAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "image", "created_at")
    list_display_links = ("id",)
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    list_per_page = 24
    actions = (accept_update,)


class GalleryUpdateAdmin(admin.ModelAdmin):
    readonly_fields = ("related_photo",)
    list_display = ("id", "user", "image", "created_at")
    list_display_links = ("id",)
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    list_per_page = 24
    actions = (accept_update,)


admin.site.register(ProfileUpdate, ProfileUpdateAdmin)
admin.site.register(MeasuresUpdate, MeasuresUpdateAdmin)
admin.site.register(ProfilePictureUpdate, ProfilePictureUpdateAdmin)
admin.site.register(CoverPictureUpdate, CoverPictureUpdateAdmin)
admin.site.register(GalleryUpdate, GalleryUpdateAdmin)
