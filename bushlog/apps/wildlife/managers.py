from django.db import models
from django.db.models import query


class SpeciesQuerySet(query.QuerySet):
    def public(self):
        return self.filter(public=True)

    def grouped_by_higher_classification(self):
        result_set = {}
        for obj in self.all():
            result_set.setdefault(obj.higher_classification, [])
            result_set[obj.higher_classification].append(obj)

        return result_set


class SpeciesManager(models.Manager):
    def get_query_set(self):
        return SpeciesQuerySet(self.model)

    def public(self):
        return self.get_query_set().public()

    def grouped_by_higher_classification(self):
        return self.get_query_set().grouped_by_higher_classification()
