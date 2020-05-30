from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import Http404

from clones.models import MeasuresClone
from .serializers import (
    MeasuresCloneSerializer
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_measures_clone(request):
    serializer = MeasuresCloneSerializer(data=request.data)
    if not serializer.is_valid():
        if 'measure' in serializer.errors:
            # The user should be able to create only one update
            res = {'measures': ['do not create a new upadte request! Update the one you have.']}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()

    # Send Email to admin
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)

class MeasuresCloneAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return MeasuresClone.objects.get(pk=pk)
        except MeasuresClone.DoesNotExist:
            raise Http404

    def get(self, request, measures_id, clone_id):
        measures_clone = self.get_object(pk=clone_id)

        # make sure that we get the measures' clone
        # owned by the logged in user
        if measures_id != measures_clone.measure.id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = MeasuresCloneSerializer(measures_clone)
        return Response(serializer.data)