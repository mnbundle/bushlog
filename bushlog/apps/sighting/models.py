from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.db import models

from bushlog.apps.location.models import Coordinate
from bushlog.apps.reserve.models import Reserve
from bushlog.apps.wildlife.models import Species
from bushlog.utils import choices


class Sighting(models.Model):
    user = models.ForeignKey(User, related_name="sightings")
    location = models.ForeignKey(Coordinate)
    reserve = models.ForeignKey(Reserve, related_name="sightings")
    species = models.ForeignKey(Species, related_name="sightings")

    date_added = models.DateTimeField(auto_now_add=True)
    date_of_sighting = models.DateTimeField()

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
        image_list = self.images.all()
        if image_list:
            return image_list[0].image
        return None

    def get_absolute_url(self):
        return reverse_lazy('sighting:index', args=[self.reserve.slug, self.species.slug, str(self.id)])


class SightingImage(models.Model):
    sighting = models.ForeignKey(Sighting, related_name="images", blank=True, null=True)
    image = models.ImageField(upload_to="sightings/%Y/%m/", max_length=250)

    def __unicode__(self):
        return unicode(self.sighting)

    def get_absolute_url(self):
        #return reverse('api', kwargs={'pk': str(self.id), 'resource_name': 'sightingimage', 'api_name': 'v1.0'})
        return "/api/v1.0/sightingimage/%s/" % self.id
