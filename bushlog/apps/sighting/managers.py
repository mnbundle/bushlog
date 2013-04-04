from django.db import models
from django.db.models import query


class SightingsQuerySet(query.QuerySet):
    def public(self):
        return self.filter(species__public=True)


class SightingManager(models.Manager):
    def get_query_set(self):
        return SightingsQuerySet(self.model)

    def public(self):
        return self.get_query_set().public()
