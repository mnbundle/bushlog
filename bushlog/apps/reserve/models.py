from django.db import models

from bushlog.apps.location.models import Coordinate
from bushlog.utils import historical_date


class Reserve(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.TextField()
    bottom_left_bound = models.ForeignKey(Coordinate, related_name="bottom_left_bound")
    top_right_bound = models.ForeignKey(Coordinate, related_name="top_right_bound")

    def __unicode__(self):
        return self.name

    @property
    def number_of_sightings(self):
        return self.sightings.filter(date_of_sighting__gte=historical_date(month=1)).count()
