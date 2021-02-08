from django.contrib import admin, messages

from updates.models import (
    ProfileUpdate,
    MeasuresUpdate,
    GalleryUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate,
)
from updates.actions import accept_update
from updates.utils import is_update_dirty


class BaseAdmin(admin.ModelAdmin):
    def get_object(self, request, object_id, from_field=None):
        obj = super().get_object(request, object_id, from_field=from_field)

        if request.method == 'GET' and is_update_dirty(obj):
            obj.purify()

        return obj

    def save_model(self, request, obj, form, change):
        update = self.get_object(request, str(obj.id))

        if is_update_dirty(update):
            update.purify()

            msg = f'your changes has not been applied. update {update.pk} has been changed since last time you viewed it.'
            # Change the messages level to ensure the success message is ingored
            messages.set_level(request, messages.WARNING)
            messages.warning(request, msg)
        else:
            return super().save_model(request, obj, form, change)


class ProfileUpdateAdmin(BaseAdmin):
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


class MeasuresUpdateAdmin(BaseAdmin):
    list_display = ("id", "measures", "created_at")
    list_display_links = ("id", "measures")
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    search_fields = ("user__email",)
    list_per_page = 24
    actions = (accept_update,)


class ProfilePictureUpdateAdmin(BaseAdmin):
    list_display = ("id", "user", "image", "created_at")
    list_display_links = ("id",)
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    list_per_page = 24
    actions = (accept_update,)


class CoverPictureUpdateAdmin(BaseAdmin):
    list_display = ("id", "user", "image", "created_at")
    list_display_links = ("id",)
    list_filter = ("created_at", "accept", "decline")
    date_hierarchy = "created_at"
    list_per_page = 24
    actions = (accept_update,)


class GalleryUpdateAdmin(BaseAdmin):
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
