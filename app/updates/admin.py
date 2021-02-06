from django.contrib import admin, messages

from updates.models import (
    ProfileUpdate,
    MeasuresUpdate,
    GalleryUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate,
)
from updates.actions import accept_update


class ProfileUpdateAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Owner', {'fields': ('user', 'profile')}),
        ('Timestamp', {"fields": ('created_at', 'changed_at')}),
        ('Update data', {'fields': ('bio',)}),
        ('Response', {"fields": ('accept', 'decline', 'message')}),
    )
    # the dirty field is just an implementation detail
    # used to track when a user modifies his intial update
    # no need to show it
    exclude = ('dirty',)
    list_display = ('id', 'user', 'created_at')
    list_display_links = ("id", "user")
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    search_fields = ("id", "user__email")
    list_per_page = 24
    readonly_fields = ('created_at', 'changed_at')
    actions = (accept_update,)

    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field=from_field)

        if obj and obj.dirty and request.method == 'GET':
            obj.dirty = False
            obj.save()

        return obj

    def save_model(self, request, obj, form, change):
        update = self.get_object(request, str(obj.id))
        # if update is dirty, stop and tell the admin
        # to check the new version. dirty is set to True
        # whenever the user changes his intial update
        if update.dirty:
            update.dirty = False
            update.save()

            # Change the messages level to ensure the success message is ingored
            messages.set_level(request, messages.WARNING)
            messages.warning(
                request,
                f'your changes has not been applied. update {update.pk} has been changed since last time you viewed it.'
            )
        else:
            return super().save_model(request, obj, form, change)


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
