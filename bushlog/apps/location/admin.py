from django.contrib import admin

from bushlog.apps.location.models import Coordinate, Country, Polygon


admin.site.register(Coordinate)
admin.site.register(Country)
admin.site.register(Polygon)
