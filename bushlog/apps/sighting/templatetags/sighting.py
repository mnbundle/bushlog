import json

from django import template

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
