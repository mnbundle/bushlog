from django import template

from bushlog.apps.profile.models import User

register = template.Library()


@register.simple_tag(takes_context=True)
def del_session(context, key):
    request = context['request']
    if key in request.session.keys():
        del request.session[key]


@register.simple_tag
def user_count():
    return User.objects.filter(is_active=True).count()
