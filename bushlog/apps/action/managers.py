from django.db import models
from django.db.models import query


class CommentQuerySet(query.QuerySet):
    def public(self):
        return self.filter(species__public=True)


class CommentManager(models.Manager):
    def get_query_set(self):
        return CommentQuerySet(self.model)

    def public(self):
        return self.get_query_set().public()
