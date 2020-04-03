from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.http import Http404

from core.models import User
from models.models import Model, Mensuration
from .serializers import ModelSerializer, UserSerializer, MeasuresSerializer, ModelSerializerWithImages
from .permissoins import IsOwner


@api_view(['GET'])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    try:
        user = request.user
        user_serializer = UserSerializer(user)
        model_serializer = ModelSerializerWithImages(user.model)
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


class ModelAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        model = self.get_object(pk=pk)
        serializer = ModelSerializer(model)
        return Response(serializer.data)

    def put(self, request, pk):
        model = self.get_object(pk=pk)
        serializer = ModelSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeasuresAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Mensuration.objects.get(pk=pk)
        except Mensuration.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        measures = self.get_object(pk=pk)
        serializer = MeasuresSerializer(measures)
        return Response(serializer.data)

    def put(self, request, pk):
        measures = self.get_object(pk=pk)
        serializer = MeasuresSerializer(measures, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
