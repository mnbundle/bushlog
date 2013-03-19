from django.core.urlresolvers import reverse_lazy
from django.db import models

from bushlog.apps.location.models import Country, Polygon
from bushlog.apps.wildlife.models import Species
from bushlog.utils import historical_date


class Reserve(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    description = models.CharField(max_length=250)
    country = models.ForeignKey(Country, related_name='users', blank=True, null=True)
    website = models.URLField()
    species = models.ManyToManyField(Species, related_name='reserves')
    border = models.ForeignKey(Polygon, related_name='reserves')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @property
    def number_of_sightings(self):
        return self.sightings.filter(date_of_sighting__gte=historical_date(month=1)).count()

    def get_absolute_url(self):
        return reverse_lazy('reserve:index', args=[self.slug])
