from django.contrib import admin

from bushlog.reserve.models import Reserve


class ReserveAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']
    prepopulated_fields = {
        'slug': ['name']
    }


admin.site.register(Reserve, ReserveAdmin)
