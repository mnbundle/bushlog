from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from bushlog.apps.activity.models import log_activity
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

    description = models.TextField()

    estimated_number = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=20, choices=choices(['male', 'female', 'both']))
    with_young = models.BooleanField(default=False)
    with_kill = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_of_sighting']

    def __unicode__(self):
        return "%s - %s" % (self.reserve, self.species)

    @property
    def mapdata(self):
        return {
            'lat': str(self.location.latitude),
            'lng': str(self.location.longitude),
            'options': {
                'icon': self.species.marker.url
            }
        }

    @property
    def cover_image(self):
        image_list = self.images.all()
        if image_list:
            return image_list[0].image
        return None


class SightingImage(models.Model):
    sighting = models.ForeignKey(Sighting, related_name="images")
    image = models.ImageField(upload_to="sightings/%Y/%m/", max_length=250)
    caption = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s - %s" % (self.sighting, self.caption)


# activity log post_save
post_save.connect(log_activity, sender=Sighting)
