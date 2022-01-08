from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Carousel, Header
from models.models import Profile, Mensuration, History


class ModelInline(admin.StackedInline):
    model = Profile


class MensurationInline(admin.StackedInline):
    model = Mensuration


class HistoryInline(admin.StackedInline):
    model = History


class OhMightyAdmin(UserAdmin):
    list_display = ('id', 'email', 'is_active')
    list_per_page = 25
    inlines = [
        ModelInline,
        HistoryInline,
        MensurationInline,
    ]
    ordering = ('email',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (_('Personal info'), {'fields': ('email', 'is_public', 'highlight')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'inUse', 'image')
    list_editable = ('inUse',)
    list_per_page = 25


class HeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'inUse', 'image')
    list_editable = ('inUse',)
    list_per_page = 25


admin.site.register(User, OhMightyAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Header, HeaderAdmin)
