from django.contrib import admin

from .models import (
    Profile,
    ProfilePicture,
    CoverPicture,
    History,
    Mensuration,
    Gallery,
    Contact,
)


class ModelAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "city", "nin", "user")
    list_display_links = ("id", "first_name")
    list_per_page = 24


class ProfilePictureAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "image", "created_at")
    list_display_links = ("id",)
    list_filter = ("inUse",)
    list_per_page = 324


class CoverPictureAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "image", "created_at")
    list_display_links = ("id",)
    list_filter = ("inUse",)
    list_per_page = 32


class HistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    list_display_links = ("id",)
    list_per_page = 24


class MensurationAdmin(admin.ModelAdmin):
    list_display = ("id", "height", "permitted", "user")
    list_display_links = ("id",)
    list_per_page = 24


class GalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "image")
    list_display_links = ("id",)
    list_filter = ("inUse",)
    list_per_page = 32


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "model_full_name",
        "model_email",
        "email",
        "phone",
        "created_at",
    )
    list_display_links = ("id", "model_full_name")
    search_fields = ("model_email", "model_full_name", "full_name", "email")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    list_per_page = 24


admin.site.register(Profile, ModelAdmin)
admin.site.register(ProfilePicture, ProfilePictureAdmin)
admin.site.register(CoverPicture, CoverPictureAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Mensuration, MensurationAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Contact, ContactAdmin)
