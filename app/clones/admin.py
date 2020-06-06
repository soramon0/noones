from django.contrib import admin

from .models import MeasuresClone, PhotoClone


class MeasuresClonedmin(admin.ModelAdmin):
    list_display = ('id', 'measure', 'taille', 'cheveux')
    list_display_links = ('id', 'measure')
    list_per_page = 24

admin.site.register(MeasuresClone, MeasuresClonedmin)
admin.site.register(PhotoClone)