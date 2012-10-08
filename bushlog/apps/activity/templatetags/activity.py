from django import template

from bushlog.apps.activity.models import Activity
from bushlog.utils import image_resize

register = template.Library()


@register.inclusion_tag("latest_activity.html")
def latest_activity(limit=50, split=False):
    obj_list = Activity.objects.all()[:limit]
    return {'obj_list': obj_list, 'split': split}
