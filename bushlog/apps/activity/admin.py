from django.contrib import admin

from bushlog.apps.activity.models import Activity


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['content_object', 'action_taken', 'date_added']
    list_display_links = ['content_object', 'action_taken']
    search_fields = ['action_taken']
    list_filter = ['date_added', 'action_taken']


admin.site.register(Activity, ActivityAdmin)
