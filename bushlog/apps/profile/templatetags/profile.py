from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def del_session(context, key):
    request = context['request']
    if key in request.session.keys():
        del request.session[key]
