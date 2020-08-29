from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, update_session_auth_hash, get_user_model

from accounts.services import confirmation_email_send
from accounts.api.serializers import (
    SigninSerializer,
    ChangePasswordSerializer,
    ChangeEmailSerializer,
)


User = get_user_model()


@api_view(("POST",))
def signin(request):
    context = {}

    serializer = SigninSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.data.get("email")
    password = serializer.data.get("password")

    user = authenticate(email=email, password=password)
    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        context["pk"] = user.pk
        context["token"] = token.key
        return Response(context)
    else:
        context["detail"] = "Invalid credentials."
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


@api_view(("PATCH",))
@permission_classes((IsAuthenticated,))
def update_password(request):
    user = request.user
    serializer = ChangePasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    password = serializer.data.get("password")
    new_password = serializer.data.get("new_password")
    confirm_password = serializer.data.get("confirm_password")

    if new_password != confirm_password:
        res = {"confirm_password": ["Passwords do not match."]}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(password):
        res = {"password": ["Wrong Password."]}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(("PATCH",))
@permission_classes((IsAuthenticated,))
def update_email(request):
    user = request.user
    serializer = ChangeEmailSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.data.get("email")

    if email == user.email:
        context = {"email": ["You did not change your email."]}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        context = {"email": ["That email is being used by another user."]}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    user.is_active = False
    user.email = email
    user.save()
    confirmation_email_send(request, user)

    return Response(status=status.HTTP_200_OK)
