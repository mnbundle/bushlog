from django.contrib import admin

from bushlog.apps.action.models import Comment, Like


admin.site.register(Comment)
admin.site.register(Like)
