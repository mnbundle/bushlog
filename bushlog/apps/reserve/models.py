from django.core.urlresolvers import reverse_lazy
from django.db import models

from bushlog.apps.location.models import Coordinate, Country
from bushlog.apps.wildlife.models import Species
from bushlog.utils import historical_date


class Reserve(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.CharField(max_length=250)
    country = models.ForeignKey(Country, related_name='users', blank=True, null=True)
    website = models.URLField(verify_exists=True)
    species = models.ManyToManyField(Species, related_name='reserves')
    bottom_left_bound = models.ForeignKey(Coordinate, related_name="bottom_left_bound")
    top_right_bound = models.ForeignKey(Coordinate, related_name="top_right_bound")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def number_of_sightings(self):
        return self.sightings.filter(date_of_sighting__gte=historical_date(month=1)).count()

    def get_absolute_url(self):
        return reverse_lazy('reserve:index', args=[self.slug])
