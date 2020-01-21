from django.contrib import admin

from .models import Model, History, Mensuratoin, Model


class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'city', 'cin')
    list_display_links = ('id', 'first_name')


admin.site.register(Model, ModelAdmin)
