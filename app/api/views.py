from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.http.request import RawPostDataException
from django.core.serializers import serialize

from models.models import Model, Mensuration, Photo, Contact
import json

def me(request):
    if not request.user.is_authenticated:
        # TODO(karim): Better handle this
        return JsonResponse({"request": "bad man"})

    return JsonResponse({
        "model": serialize("json", [request.user.model]),
        "email": request.user.email,
    })
