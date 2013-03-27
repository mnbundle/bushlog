from django.contrib import admin

from bushlog.apps.reserve.models import Reserve


class ReserveAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_display_links = ['name']
    search_fields = ['name', 'country']
    prepopulated_fields = {
        'slug': ['name']
    }


admin.site.register(Reserve, ReserveAdmin)
