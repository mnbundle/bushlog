from django import template

from bushlog.apps.action.models import Comment, Like

register = template.Library()


@register.inclusion_tag("template_tags/like_button.html", takes_context=True)
def like_button(context):
    obj = context['object']
    user = context['request'].user
    obj_list = Like.by_object(obj)

    if user.is_authenticated():
        context['liked'] = bool(obj_list.filter(user=user))
    context['like_count'] = obj_list.count()
    context['obj_type'] = obj.__class__.__name__.lower()

    return context


@register.simple_tag
def like_count():
    return Like.objects.all().count()


@register.inclusion_tag("template_tags/comments.html", takes_context=True)
def comments(context):
    obj = context['object']
    obj_list = Comment.by_object(obj)

    context['comment_count'] = obj_list.count()
    context['object_type'] = obj.__class__.__name__.lower()
    context['comment_list'] = obj_list

    return context


@register.simple_tag
def comment_count():
    return Comment.objects.all().count()
