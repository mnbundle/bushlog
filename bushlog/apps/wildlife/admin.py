from django.contrib import admin

from bushlog.apps.reserve.models import Reserve
from bushlog.apps.wildlife.models import Species, SpeciesInfo


class ReserveInline(admin.TabularInline):
    model = Reserve.species.through


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['public', 'common_name', 'scientific_name']
    list_display_links = ['common_name', 'scientific_name']
    search_fields = ['common_name', 'scientific_name']
    list_filter = ['public', 'reserves']
    prepopulated_fields = {
        'slug': ['common_name']
    }
    inlines = [ReserveInline]


admin.site.register(Species, SpeciesAdmin)
admin.site.register(SpeciesInfo)
