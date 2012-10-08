from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from bushlog.utils import choices


class Activity(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    date_added = models.DateTimeField(auto_now_add=True)
    action_taken = models.CharField(max_length=30, choices=choices(['user_added', 'sighting_added']))

    class Meta:
        ordering = ['-date_added']
        verbose_name_plural = "Activies"

    def __unicode__(self):
        return "%s %s" % (self.content_object, self.action_taken)


# activity log post_save method
def log_activity(sender, instance, created, **kwargs):
    action_taken = None
    if sender.__name__ == "Sighting":
        action_taken = "sighting_added"
    elif sender.__name__ == "UserProfile":
        action_taken = "user_added"

    if created and action_taken:
        Activity.objects.create(
            content_object=instance,
            action_taken=action_taken
        )
