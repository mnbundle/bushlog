import json

from django.http import HttpResponseBadRequest, HttpResponse


def json_response(func):
    """
    Ensures the request is an ajax request and the response is returned as json.
    """
    def wrap(kls, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return HttpResponse(
            json.dumps(func(kls, request, *args, **kwargs)), status=200, content_type='application/json'
        )
    return wrap
