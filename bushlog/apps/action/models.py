from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models

from bushlog.apps.action.managers import CommentManager


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


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comments")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    comment = models.TextField(max_length=1000)
    public = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-date_added']
        get_latest_by = 'date_added'

    @classmethod
    def by_object(cls, obj):
        return cls.objects.filter(content_type__model=obj.__class__.__name__.lower(), object_id=obj.pk)

    def __unicode__(self):
        return "%s (%s)" % (self.content_object, self.user)
