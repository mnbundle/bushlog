from django.db import models
from django.db.models import query


class ReserveQuerySet(query.QuerySet):
    def grouped_by_country(self):
        result_set = {}
        for obj in self.all():
            for country in obj.country.all().order_by('name'):
                result_set.setdefault(country.name, [])
                result_set[country.name].append(obj)

        return result_set


class ReserveManager(models.Manager):
    def get_query_set(self):
        return ReserveQuerySet(self.model)

    def grouped_by_country(self):
        return self.get_query_set().public()
