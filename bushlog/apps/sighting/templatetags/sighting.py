import json

from django import template

from bushlog.apps.sighting.models import Sighting
from bushlog.utils import image_resize

register = template.Library()


@register.simple_tag(takes_context=True)
def latest_sightings_mapdata(context, reserve=None):
    if reserve:
        obj_list = Sighting.objects.filter(reserve=reserve)[:5]
    else:
        obj_list = Sighting.objects.all()[:5]

    return json.dumps([obj.mapdata for obj in obj_list])


@register.simple_tag
def resize_image(image, width, height):
    return image_resize(image, width, height)
