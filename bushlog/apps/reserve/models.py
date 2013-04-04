from django.core.urlresolvers import reverse_lazy
from django.db import models

from bushlog.apps.location.models import Country, Polygon
from bushlog.apps.wildlife.models import Species
from bushlog.utils import historical_date, point_in_polygon


class Reserve(models.Model):
    species = models.ManyToManyField(Species, related_name='reserves')
    border = models.ForeignKey(Polygon, related_name='reserves')
    country = models.ManyToManyField(Country, related_name='reserves')

    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.CharField(max_length=250)
    website = models.URLField()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def number_of_sightings(self):
        return self.sightings.filter(date_of_sighting__gte=historical_date(month=1)).count()

    def sighting_in_reserve(self, coordinates):
        latitude = float(coordinates['latitude'])
        longitude = float(coordinates['longitude'])

        return point_in_polygon(latitude, longitude, self.border.points)

    def get_absolute_url(self):
        return reverse_lazy('reserve:index', args=[self.slug])
