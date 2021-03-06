import datetime
import json

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import Sighting
from bushlog.utils import fuzzydate, image_resize, historical_date

register = template.Library()


@register.simple_tag(takes_context=True)
def latest_sightings_mapdata(context, limit=3, *args, **kwargs):
    if kwargs:
        obj_list = Sighting.objects.public().active().filter(**kwargs)[:limit]
    else:
        obj_list = Sighting.objects.public().active()[:limit]

    return json.dumps([obj.mapdata for obj in obj_list])


@register.simple_tag
def resize_image(image, width=None, height=None):
    return image_resize(image, width=width, height=height)


@register.inclusion_tag("template_tags/sighting_map.html", takes_context=True)
def sighting_map(context, limit=3, protected=1, dashboard=0, *args, **kwargs):
    try:
        if len(kwargs.keys()) > 1:
            keyword = "list"
        else:
            keyword = kwargs.keys()[0]
    except IndexError:
        keyword = None

    coordinates = kwargs.get('coordinates')
    bounds = []

    if kwargs:
        if coordinates:
            object_list = [
                obj for obj in Sighting.objects.public().active().filter(date_of_sighting__gte=historical_date(weeks=1))
                if obj.in_proximity(coordinates['latitude'], coordinates['longitude'], 0.3)
            ]

            try:
                context['object'] = [obj for obj in Reserve.objects.all() if obj.sighting_in_reserve(coordinates)][0]
                keyword = 'reserve'
            except IndexError:
                pass

        else:
            object_list = Sighting.objects.filter(**kwargs)
            if not 'pk' in kwargs.keys():
                object_list = object_list.active()
            if protected:
                object_list = object_list.public()

        reserve = kwargs.get('reserve')

        if reserve:
            bounds = [
                [value['latitude'], value['longitude']] for key, value in reserve.bounds.items()
                if key != 'center_point'
            ]

    else:
        object_list = Sighting.objects.active()
        if protected:
            object_list = object_list.public()

    mapdata = [obj.mapdata for obj in object_list[:limit]]
    if coordinates:
        mapdata.append({
            'lat': str(coordinates['latitude']),
            'lng': str(coordinates['longitude']),
            'options': {
                'icon': '/media/markers/user.png'
            },
            'data': {
                'href': '/sighting/search/%s/%s/' % (
                    coordinates['latitude'],
                    coordinates['longitude']
                )
            }
        })

    context.update({
        'object': context.get('object'),
        'mapdata': json.dumps(mapdata),
        'heatmapdata': json.dumps([obj.heatmapdata for obj in object_list]),
        'bounds': json.dumps(bounds),
        'keyword': keyword,
        'coordinates': coordinates,
        'dashboard': dashboard,
        'context': context
    })

    return context


@register.inclusion_tag("template_tags/latest_sightings.html", takes_context=True)
def latest_sightings(context, split=1, limit=3, offset=0, protected=1, exclude_pk={}, *args, **kwargs):
    try:
        keyword = kwargs.keys()[0]
    except IndexError:
        keyword = None

    if exclude_pk:
        keyword = 'exclude_pk'

    coordinates = kwargs.get('coordinates')

    if kwargs:
        if coordinates:
            object_list = [
                obj for obj in Sighting.objects.public().active().filter(date_of_sighting__gte=historical_date(weeks=1))
                if obj.in_proximity(coordinates['latitude'], coordinates['longitude'], 0.3)
            ]
        else:
            object_list = Sighting.objects.active().filter(**kwargs)
            if protected:
                object_list = object_list.public()

    else:
        object_list = Sighting.objects.active()
        if protected:
            object_list = object_list.public()

    if exclude_pk:
        object_list = object_list.exclude(pk=exclude_pk)

    context.update({
        'object': context.get('object'),
        'object_list': object_list[offset:limit],
        'split': split,
        'offset': offset,
        'keyword': keyword
    })

    return context


@register.filter
def fuzzy_date(timestamp, to=None):
    return fuzzydate(timestamp, to)


@register.simple_tag
def sighting_count():
    return intcomma(Sighting.objects.active().count())
