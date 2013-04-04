from django import template

from bushlog.apps.reserve.models import Reserve

register = template.Library()


@register.inclusion_tag("template_tags/featured_reserve_maps.html")
def featured_reserve_maps(limit=3):
    obj_list = sorted(Reserve.objects.all(), key=lambda obj: obj.number_of_sightings, reverse=True)[:limit]
    return {'obj_list': obj_list}


@register.simple_tag
def reserve_count():
    return Reserve.objects.all().count()


@register.simple_tag
def reserve_country_count():
    countries = []
    for obj in Reserve.objects.all():
        for country in obj.country.all():
            if country.name not in countries:
                countries.append(country.name)

    return len(countries)
