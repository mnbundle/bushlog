from django.db import models
from django.db.models import query


class SpeciesQuerySet(query.QuerySet):
    def public(self):
        return self.filter(public=True)


class SpeciesManager(models.Manager):
    def get_query_set(self):
        return SpeciesQuerySet(self.model)

    def public(self):
        return self.get_query_set().public()
