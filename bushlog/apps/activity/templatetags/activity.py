from django import template

from bushlog.apps.activity.models import Activity
from bushlog.utils import image_resize

register = template.Library()


@register.inclusion_tag("latest_activity.html")
def latest_activity(limit=20):
    obj_list = Activity.objects.all()[:3]
    return {'obj_list': obj_list}
