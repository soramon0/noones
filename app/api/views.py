from django.http import HttpResponseBadRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import User
from .serializers import ModelSerializer, UserSerializer, MeasuresSerializer


@api_view(['GET'])
def me(request):
    if not request.user.is_authenticated:
        # TODO(karim): Better handle this
        return Response({"request": "bad man"})

    try:
        user_serializer = UserSerializer(request.user, many=False)
        model_serializer = ModelSerializer(request.user.model, many=False)
        measures_serializer = MeasuresSerializer(
            request.user.model.measures, many=False)

        res = {
            'model': model_serializer.data
        }

        res['model'].update({'email': user_serializer.data['email']})
        res['measures'] = measures_serializer.data

        return Response(res)

    except User.model.RelatedObjectDoesNotExist:
        # Handling when admin user logs in
        # admin does't have the requried fields for this page
        # So we redirect him
        # TODO(karim): handle the navigation to not include a link to this page
        return HttpResponseBadRequest(Response({"request": "unauthorized"}))
