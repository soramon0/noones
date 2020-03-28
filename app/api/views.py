from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.http.request import RawPostDataException
from django.core.serializers import serialize
from django.http import HttpResponseBadRequest

from models.models import Model, Mensuration, Photo, Contact
from core.models import User
import json

def me(request):
    if not request.user.is_authenticated:
        # TODO(karim): Better handle this
        return JsonResponse({"request": "bad man"})

    try:
        res = {
            "model": serialize("json", [request.user.model]),
            "email": request.user.email,
        }
        return JsonResponse(res)
    except User.model.RelatedObjectDoesNotExist:
        # Handling when admin user logs in
        # admin does't have the requried fields for this page
        # So we redirect him
        # TODO(karim): handle the navigation to not include a link to this page
        return HttpResponseBadRequest(JsonResponse({"request": "unauthorized"}))

    
