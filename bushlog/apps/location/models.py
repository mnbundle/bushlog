import json

from django.db import models


class Coordinate(models.Model):
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)

    def __unicode__(self):
        return "%s,%s" % (self.latitude, self.longitude)

    def as_json(self):
        return json.dumps({
            'latlng': [str(self.latitude), str(self.longitude)]
        })
