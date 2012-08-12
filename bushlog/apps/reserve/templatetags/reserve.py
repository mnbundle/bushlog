from django import template

from bushlog.apps.reserve.models import Reserve

register = template.Library()


@register.inclusion_tag("featured_reserve_maps.html")
def featured_reserve_maps(limit=3):
    obj_list = sorted(Reserve.objects.all(), key=lambda obj: obj.number_of_sightings)[:3]
    return {'obj_list': obj_list}
