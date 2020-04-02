from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import User
from .serializers import ModelSerializer, UserSerializer, MeasuresSerializer


class ModelAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            user_serializer = UserSerializer(user)
            model_serializer = ModelSerializer(user.model)
            measures_serializer = MeasuresSerializer(user.model.measures)

            res = {'model': model_serializer.data}
            res['model'].update({'email': user_serializer.data['email']})
            res['measures'] = measures_serializer.data

            return Response(res)

        except User.model.RelatedObjectDoesNotExist:
            # Handling when admin user logs in
            # admin does't have the requried fields for this page
            # So we redirect him
            # TODO(karim): handle the navigation to not include a link to this page
            return Response(status=status.HTTP_401_UNAUTHORIZED)
