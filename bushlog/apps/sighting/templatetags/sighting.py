import datetime
import json

from django import template
from django.utils.translation import ungettext, ugettext

from bushlog.apps.reserve.models import Reserve
from bushlog.apps.sighting.models import Sighting
from bushlog.utils import image_resize, historical_date

register = template.Library()


@register.simple_tag(takes_context=True)
def latest_sightings_mapdata(context, limit=3, *args, **kwargs):
    if kwargs:
        obj_list = Sighting.objects.filter(**kwargs)[:limit]
    else:
        obj_list = Sighting.objects.all()[:limit]

    return json.dumps([obj.mapdata for obj in obj_list])


@register.simple_tag
def resize_image(image, width=None, height=None):
    return image_resize(image, width=width, height=height)


@register.inclusion_tag("template_tags/sighting_map.html", takes_context=True)
def sighting_map(context, limit=3, *args, **kwargs):
    try:
        keyword = kwargs.keys()[0]
    except IndexError:
        keyword = None

    coordinates = kwargs.get('coordinates')

    if kwargs:
        if coordinates:
            obj_list = [
                obj for obj in Sighting.objects.filter(date_of_sighting__gte=historical_date(day=1))
                if obj.in_proximity(coordinates['latitude'], coordinates['longitude'], 0.3)
            ][:limit]

            try:
                context['object'] = [obj for obj in Reserve.objects.all() if obj.sighting_in_reserve(coordinates)][0]
                keyword = 'reserve'
            except IndexError:
                pass

        else:
            obj_list = Sighting.objects.filter(**kwargs)[:limit]
    else:
        obj_list = Sighting.objects.all()[:limit]

    mapdata = [obj.mapdata for obj in obj_list]
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

    return {
        'object': context.get('object'),
        'mapdata': json.dumps(mapdata),
        'keyword': keyword,
        'coordinates': coordinates
    }


@register.inclusion_tag("template_tags/latest_sightings.html", takes_context=True)
def latest_sightings(context, split=1, limit=3, exclude_pk={}, *args, **kwargs):
    try:
        keyword = kwargs.keys()[0]
    except IndexError:
        keyword = None

    coordinates = kwargs.get('coordinates')

    if kwargs:
        if coordinates:
            object_list = [
                obj for obj in Sighting.objects.filter(date_of_sighting__gte=historical_date(day=1))
                if obj.in_proximity(coordinates['latitude'], coordinates['longitude'], 0.3)
            ]
        else:
            object_list = Sighting.objects.filter(**kwargs)
    else:
        object_list = Sighting.objects.all()

    if exclude_pk:
        object_list = object_list.exclude(pk=exclude_pk)

    return {
        'object': context.get('object'),
        'object_list': object_list[:limit],
        'split': split,
        'keyword': keyword
    }


@register.filter
def fuzzy_date(timestamp, to=None):
    if not timestamp:
        return ""

    compare_with = to or datetime.date.today()
    delta = timestamp - compare_with

    if delta.days == 0:
        return u"today"
    elif delta.days == -1:
        return u"yesterday"
    elif delta.days == 1:
        return u"tomorrow"

    chunks = (
        (365.0, lambda n: ungettext('year', 'years', n)),
        (30.0, lambda n: ungettext('month', 'months', n)),
        (7.0, lambda n: ungettext('week', 'weeks', n)),
        (1.0, lambda n: ungettext('day', 'days', n)),
    )

    for i, (chunk, name) in enumerate(chunks):
        if abs(delta.days) >= chunk:
            count = abs(round(delta.days / chunk, 0))
            break

    date_str = ugettext('%(number)d %(type)s') % {'number': count, 'type': name(count)}

    if delta.days > 0:
        return "in " + date_str
    else:
        return date_str + " ago"


@register.simple_tag
def sighting_count():
    return Sighting.objects.all().count()
