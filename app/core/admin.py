from django.contrib import admin

from .models import User, Carousel, Header


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_active')
    list_per_page = 25
    list_filter = ('email', 'is_active')


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('id', 'inUse', 'image')
    list_editable = ('inUse',)
    list_per_page = 25


class HeaderAdmin(admin.ModelAdmin):
    list_display = ('id', 'inUse', 'image')
    list_editable = ('inUse',)
    list_per_page = 25


admin.site.register(User, UserAdmin)
admin.site.register(Carousel, CarouselAdmin)
admin.site.register(Header, HeaderAdmin)
