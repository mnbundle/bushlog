from django.db import models

from bushlog.utils import choices


class SpeciesInfo(models.Model):
    height = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    length = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    mass = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)
    horn_length = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)

    def __unicode__(self):
        return "%s(mass), %s(height), %s(length), %s(horn length)" % (
            self.mass,
            self.height,
            self.length,
            self.horn_length
        )


class Species(models.Model):
    common_name = models.CharField(max_length=75)
    scientific_name = models.CharField(max_length=75)
    slug = models.SlugField()
    marker = models.ImageField(upload_to="markers/", max_length=250)
    default_image = models.ImageField(upload_to="defaults/", max_length=250)

    classification = models.CharField(max_length=20, choices=choices(['carnivore', 'herbivore', 'omnivore']))
    general_info = models.TextField()
    female_info = models.ForeignKey(SpeciesInfo, related_name="female_info")
    male_info = models.ForeignKey(SpeciesInfo, related_name="male_info")

    similiar_species = models.ManyToManyField("self", related_name="similiar_species", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Species"

    def __unicode__(self):
        return "%s (%s)" % (self.common_name, self.scientific_name)
