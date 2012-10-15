from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey

from bushlog.apps.profile.models import Notification, UserProfile


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['type', 'subject']
    list_display_links = ['type', 'subject']
    search_fields = ['type', 'subject']


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [UserProfileInline, ApiKeyInline]


admin.site.unregister(User)
admin.site.register(ApiKey)
admin.site.register(ApiAccess)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Notification, NotificationAdmin)
