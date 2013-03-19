import json

from django.db import models


class Polygon(models.Model):
    def __unicode__(self):
        return "%s" % (self.id)

    def as_json(self):
        return json.dumps({
            'polygon': [[coordinate.latitude, coordinate.longitude] for coordinate in self.coordinates.all()]
        })


class Coordinate(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    polygon = models.ForeignKey(Polygon, related_name='coordinates', blank=True, null=True)

    def __unicode__(self):
        return "%s,%s" % (self.latitude, self.longitude)

    def as_json(self):
        return json.dumps({
            'latlng': [str(self.latitude), str(self.longitude)]
        })


class Country(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name
