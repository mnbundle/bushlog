from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models


class Like(models.Model):
    user = models.ForeignKey(User, related_name="likes")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    @classmethod
    def by_object(cls, obj):
        return cls.objects.filter(content_type__model=obj.__class__.__name__.lower(), object_id=obj.pk)

    def __unicode__(self):
        return "%s (%s)" % (self.content_object, self.user)
