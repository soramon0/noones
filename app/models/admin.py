from django.contrib import admin

from .models import Model, History, Mensuration, Photo


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'city', 'cin', 'user')
    list_display_links = ('id', 'first_name')


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_display_links = ('id',)


class MensurationAdmin(admin.ModelAdmin):
    list_display = ('id', 'taille', 'cheveux', 'permitted', 'user')
    list_display_links = ('id', 'taille', 'permitted')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'image')
    list_display_links = ('id',)


admin.site.register(Model, ModelAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Mensuration, MensurationAdmin)
admin.site.register(Photo, PhotoAdmin)
