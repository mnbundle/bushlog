from django.contrib import admin

from bushlog.wildlife.models import Species, SpeciesInfo


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ['common_name', 'scientific_name']
    list_display_links = ['common_name', 'scientific_name']
    search_fields = ['common_name', 'scientific_name']
    prepopulated_fields = {
        'slug': ['common_name']
    }


admin.site.register(Species, SpeciesAdmin)
admin.site.register(SpeciesInfo)
