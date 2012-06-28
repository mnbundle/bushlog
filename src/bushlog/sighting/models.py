from django.contrib.auth.models import User
from django.db import models

from bushlog.location.models import Coordinate
from bushlog.reserve.models import Reserve
from bushlog.wildlife.models import Species


class Sighting(models.Model):
    user = models.ForeignKey(User, related_name="sightings")
    location = models.ForeignKey(Coordinate)
    reserve = models.ForeignKey(Reserve, related_name="sightings")
    species = models.ForeignKey(Species, related_name="sightings")
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_of_sighting = models.DateTimeField()
    
    description = models.TextField()
    
    estimated_number = models.IntegerField(blank=True, null=True)
    with_young = models.BooleanField(default=False)
    with_kill = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s - %s" % (self.reserve, self.species)

class SightingImage(models.Model):
    sighting = models.ForeignKey(Sighting, related_name="images")
    image = models.ImageField(upload_to="sightings/%Y/%m/", max_length=250)
    caption = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s - %s" % (self.sighting, self.caption)
