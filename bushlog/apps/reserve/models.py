from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy
from django.db import models

from bushlog.apps.location.models import Country, Polygon
from bushlog.apps.wildlife.models import Species
from bushlog.utils import generate_key, historical_date, point_in_polygon


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
        return self.sightings.public().active().filter(date_of_sighting__gte=historical_date(month=1)).count()

    @property
    def bounds(self):
        cache_key = generate_key(self, 'bounds')
        obj = cache.get(cache_key)

        if not obj:
            points = self.border.points
            latitudes = [p[0] for p in points]
            longitudes = [p[1] for p in points]

            north_bound = min(latitudes)
            south_bound = max(latitudes)
            west_bound = max(longitudes)
            east_bound = min(longitudes)

            obj = {
                'north_west': {
                    'latitude': north_bound,
                    'longitude': west_bound
                },
                'north_east': {
                    'latitude': north_bound,
                    'longitude': east_bound
                },
                'south_west': {
                    'latitude': south_bound,
                    'longitude': west_bound
                },
                'south_east': {
                    'latitude': south_bound,
                    'longitude': east_bound
                },
                'centre_point': {
                    'latitude': north_bound - ((north_bound - south_bound) / 2),
                    'longitude': west_bound - ((west_bound - east_bound) / 2)
                }
            }
            cache.set(cache_key, obj)

        return obj

    @property
    def bounding_box(self):
        bounds = self.bounds
        return [
            bounds['south_east']['longitude'],
            bounds['north_west']['latitude'],
            bounds['north_west']['longitude'],
            bounds['south_east']['latitude'],
        ]

    def sighting_in_reserve(self, coordinates):
        latitude = float(coordinates['latitude'])
        longitude = float(coordinates['longitude'])

        return point_in_polygon(latitude, longitude, self.border.points)

    def get_absolute_url(self):
        return reverse_lazy('reserve:index', args=[self.slug])

