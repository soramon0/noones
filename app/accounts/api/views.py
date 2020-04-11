from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .permissions import IsOwner
from core.models import User
from models.models import Model, Mensuration, Photo

@api_view(['POST'])
def signin(request):
    context = {}

    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        context['pk'] = user.pk
        context['token'] = token.key
        return Response(context)
    else:
        context['detail'] = 'Invalid credentials'
        return Response(context, status=status.HTTP_400_BAD_REQUEST)