from django.contrib.contenttypes.models import ContentType
from django.views import generic

from bushlog.apps.action.models import Like
from bushlog.apps.sighting.models import Sighting
from bushlog.decorators import json_response


class LikeView(generic.View):

    @json_response
    def post(self, request, *args, **kwargs):
        object_id = request.POST.get('id')
        model_name = kwargs.get('type')

        model_map = {
            'sighting': Sighting,
        }

        try:
            model = model_map[model_name].objects.get(id=object_id)
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
        }

like = LikeView.as_view()
