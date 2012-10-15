from django.contrib import admin

from bushlog.apps.location.models import Coordinate, Country


admin.site.register(Coordinate)
admin.site.register(Country)
