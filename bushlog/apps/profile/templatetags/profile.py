from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from bushlog.apps.profile.models import User

register = template.Library()


@register.simple_tag(takes_context=True)
def del_session(context, key):
    request = context['request']
    if key in request.session.keys():
        del request.session[key]
    return ''


@register.simple_tag
def user_count():
    return intcomma(User.objects.filter(is_active=True).count())


@register.simple_tag
def user_sighting_count(user):
    return intcomma(user.sightings.active().count())


@register.simple_tag
def user_comment_count(user):
    return intcomma(user.comments.all().count())
