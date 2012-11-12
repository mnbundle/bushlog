import datetime
import json

from django import template
from django.utils.translation import ungettext, ugettext

from bushlog.apps.sighting.models import Sighting
from bushlog.utils import image_resize

register = template.Library()


@register.simple_tag(takes_context=True)
def latest_sightings_mapdata(context, limit=3, *args, **kwargs):
    if kwargs:
        obj_list = Sighting.objects.filter(**kwargs)[:limit]
    else:
        obj_list = Sighting.objects.all()[:limit]

    return json.dumps([obj.mapdata for obj in obj_list])


@register.simple_tag
def resize_image(image, width, height):
    return image_resize(image, width, height)


@register.inclusion_tag("template_tags/sighting_map.html", takes_context=True)
def sighting_map(context, limit=3, *args, **kwargs):
    try:
        keyword = kwargs.keys()[0]
    except IndexError:
        keyword = None

    if kwargs:
        obj_list = Sighting.objects.filter(**kwargs)[:limit]
    else:
        obj_list = Sighting.objects.all()[:limit]

    return {
        'object': context['object'],
        'mapdata': json.dumps([obj.mapdata for obj in obj_list]),
        'keyword': keyword
    }


@register.inclusion_tag("template_tags/latest_sightings.html", takes_context=True)
def latest_sightings(context, split=False, limit=3, *args, **kwargs):
    try:
        keyword = kwargs.keys()[0]
    except IndexError:
        keyword = None

    if kwargs:
        obj_list = Sighting.objects.filter(**kwargs)[:limit]
    else:
        obj_list = Sighting.objects.all()[:limit]

    return {'obj_list': obj_list, 'split': split, 'keyword': keyword}


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
