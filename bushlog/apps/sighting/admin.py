from django.contrib import admin

from bushlog.apps.sighting.models import Sighting, SightingImage


class SightingImageTabularInline(admin.TabularInline):
    model = SightingImage


class SightingAdmin(admin.ModelAdmin):
    list_display = ['species', 'reserve', 'user', 'with_young', 'with_kill', 'date_of_sighting']
    list_display_links = ['species', 'reserve', 'user']
    search_fields = ['species', 'reserve', 'user', 'date_of_sighting']
    list_filter = ['with_young', 'with_kill', 'reserve']
    inlines = [SightingImageTabularInline]


admin.site.register(Sighting, SightingAdmin)
admin.site.register(SightingImage)
