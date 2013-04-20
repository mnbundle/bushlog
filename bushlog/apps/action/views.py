from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django.views import generic

from bushlog.apps.action.models import Comment, Like
from bushlog.apps.sighting.models import Sighting
from bushlog.decorators import json_response
from bushlog.utils import fuzzydate, image_resize


MODELMAP = {
    'sighting': Sighting,
}


class LikeView(generic.View):

    @json_response
    def post(self, request, *args, **kwargs):
        object_id = request.POST.get('id')

        if not object_id:
            return {
                'success': False,
            }

        model_name = kwargs.get('type')

        try:
            model = MODELMAP[model_name].objects.get(id=object_id)
        except IndexError:
            return {
                'success': False,
            }

        content_type = ContentType.objects.get_for_model(model)

        obj, created = Like.objects.get_or_create(
            object_id=object_id,
            content_type=content_type,
            user=request.user
        )

        return {
            'success': created,
            'object': {
                'id': obj.id,
                'user': {
                    "id": obj.user.id,
                    "username": obj.user.username,
                    "gender": obj.user.profile.gender.lower() if obj.user.profile.gender else 'male',
                    "avatar": image_resize(obj.user.profile.avatar, 35, 35) if obj.user.profile.avatar else None,
                    "url": unicode(obj.user.profile.get_absolute_url())
                },
                'object_id': obj.id
            },
        }


class CommentView(generic.View):

    @json_response
    def post(self, request, *args, **kwargs):
        object_id = request.POST.get('id')
        comment = request.POST.get('comment')

        if not comment or not object_id:
            return {
                'success': False,
            }

        model_name = kwargs.get('type')

        try:
            model = MODELMAP[model_name].objects.get(id=object_id)
        except IndexError:
            return {
                'success': False,
            }

        content_type = ContentType.objects.get_for_model(model)

        obj, created = Comment.objects.get_or_create(
            object_id=object_id,
            content_type=content_type,
            user=request.user,
            comment=comment
        )

        return {
            'success': created,
            'object': {
                'id': obj.id,
                'user': {
                    "id": obj.user.id,
                    "username": obj.user.username,
                    "gender": obj.user.profile.gender.lower() if obj.user.profile.gender else 'male',
                    "avatar": image_resize(obj.user.profile.avatar, 35, 35) if obj.user.profile.avatar else None,
                    "url": unicode(obj.user.profile.get_absolute_url())
                },
                'comment': obj.comment,
                'fuzzy_date_added': fuzzydate(obj.date_added.date())
            }
        }

    @json_response
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            obj = get_object_or_404(Comment, pk=pk)
            if (request.user.is_superuser) or (request.user == obj.user) or (request.user == obj.content_object.user):
                obj.delete()
                return {
                    'success': True,
                }

        return {
            'success': False,
        }

like = LikeView.as_view()
comment = CommentView.as_view()
