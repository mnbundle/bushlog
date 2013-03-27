from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import models

from bushlog.apps.location.models import Coordinate
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.wildlife.models import Species
from bushlog.utils import choices, get_exif_data, get_gps_data


class Sighting(models.Model):
    user = models.ForeignKey(User, related_name="sightings")
    location = models.ForeignKey(Coordinate)
    reserve = models.ForeignKey(Reserve, related_name="sightings")
    species = models.ForeignKey(Species, related_name="sightings")

    date_added = models.DateTimeField(auto_now_add=True)
    date_of_sighting = models.DateTimeField()
    public = models.BooleanField(default=True)

    description = models.TextField(blank=True, null=True)

    estimated_number = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=20, choices=choices(['Male', 'Female', 'Both']), blank=True, null=True)
    with_young = models.BooleanField(default=False)
    with_kill = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_of_sighting']
        get_latest_by = 'date_of_sighting'

    def __unicode__(self):
        return "%s - %s" % (self.reserve, self.species)

    @property
    def mapdata(self):
        """
        Return required map data for use in Google maps.
        """
        return {
            'lat': str(self.location.latitude),
            'lng': str(self.location.longitude),
            'options': {
                'icon': self.species.marker.url
            },
            'data': {
                'href': str(self.get_absolute_url())
            }
        }

    @property
    def cover_image(self):
        """
        Returns the first image as a cover image.
        """
        image_list = self.images.all()
        if image_list:
            return image_list[0].image
        return None

    def in_proximity(self, latitude, longitude, radius):
        point_latitude = float(self.location.latitude)
        point_longitude = float(self.location.longitude)

        return ((float(latitude) - point_latitude) ** 2 + (float(longitude) - point_longitude) ** 2) <= radius ** 2

    def get_absolute_url(self):
        return reverse_lazy('sighting:index', args=[self.reserve.slug, self.species.slug, str(self.id)])


class SightingImage(models.Model):
    sighting = models.ForeignKey(Sighting, related_name="images", blank=True, null=True)
    image = models.ImageField(upload_to="sightings/%Y/%m/", max_length=250)

    def __unicode__(self):
        return unicode(self.sighting)

    @property
    def exif_data(self):
        return get_exif_data(self.image.path)

    @property
    def gps_data(self):
        return get_gps_data(self.image.path)

    def get_absolute_url(self):
        return reverse_lazy('api:sightingimage_detail', args=[self.pk])
