from django.contrib import admin

from bushlog.apps.sighting.models import Sighting, SightingImage


class SightingImageTabularInline(admin.TabularInline):
    model = SightingImage


class SightingAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'species', 'reserve', 'user', 'with_young', 'with_kill', 'date_of_sighting']
    list_display_links = ['species', 'reserve', 'user']
    search_fields = ['id', 'species__common_name', 'reserve__name', 'user__username', 'date_of_sighting']
    list_filter = ['is_active', 'with_young', 'with_kill']
    inlines = [SightingImageTabularInline]


admin.site.register(Sighting, SightingAdmin)
admin.site.register(SightingImage)
