from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from bushlog.apps.reserve.models import Reserve
from bushlog.utils import get_weather_data

register = template.Library()


@register.inclusion_tag("template_tags/featured_reserve_maps.html", takes_context=True)
def featured_reserve_maps(context, limit=3):
    obj_list = sorted(
        Reserve.objects.exclude(sightings__isnull=True), key=lambda obj: obj.number_of_sightings, reverse=True
    )[:limit]

    return {'obj_list': obj_list}


@register.inclusion_tag("template_tags/reserve_weather.html", takes_context=True)
def reserve_weather(context):
    centre_point = context['object'].bounds['centre_point']
    weather_data = get_weather_data(centre_point['latitude'], centre_point['longitude'])

    return {'weather_data': weather_data}


@register.simple_tag
def reserve_count():
    return intcomma(Reserve.objects.all().count())


@register.simple_tag
def reserve_country_count():
    countries = []
    for obj in Reserve.objects.all():
        for country in obj.country.all():
            if country.name not in countries:
                countries.append(country.name)

    return len(countries)
