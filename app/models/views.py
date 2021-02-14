from django.shortcuts import render, get_object_or_404
from rest_framework import status
from django.contrib.auth import get_user_model

from pages.forms import SearchForm
from models.forms import ModelContactForm
from models.models import (
    Profile,
    Mensuration,
    Gallery,
    Contact,
    ProfilePicture,
    CoverPicture,
)

User = get_user_model()


def list_models(request):
    fields = ('image', 'profile__first_name', 'profile__last_name',
              'profile__country', 'profile__city')
    models = (
        ProfilePicture.objects.filter(inUse=True, user__is_public=True)
        .select_related('profile')
        .only(*fields)
        .order_by("-user__created_at")[:12]
    )
    context = {"data": models, "form": SearchForm()}

    return render(request, "models/index.html", context)


def detail_model(request, id):
    fields = (
        "profile__first_name",
        "profile__last_name",
        "profile__country",
        "profile__city",
        "profile__bio",
        "mensuration",
    )
    query = User.objects.only(*fields).filter(is_public=True)
    user = get_object_or_404(query, profile=id)
    model = user.profile
    photos = Gallery.objects.only("image").filter(user_id=user.id)[:8]

    context = {
        "model": model,
        "measures": user.mensuration,
        "photos": photos,
        "form": ModelContactForm(
            initial={
                "model_id": model.id,
                "model_full_name": f"{model.first_name} {model.last_name}",
            }
        ),
    }

    try:
        profile_picture = ProfilePicture.objects.only("image").get(
            user_id=user.id, inUse=True
        )

        context["profile"] = profile_picture.image.url
    except ProfilePicture.DoesNotExist:
        context["profile"] = None

    try:
        cover_picture = CoverPicture.objects.only("image").get(
            user_id=user.id, inUse=True
        )
        context["cover"] = cover_picture.image.url
    except CoverPicture.DoesNotExist:
        context["cover"] = None

    return render(request, "models/model.html", context)


def search_models(request):
    form = SearchForm(request.GET)

    if not form.is_valid():
        context = {
            "form": form,
        }
        return render(
            request, "models/search.html", context, status=status.HTTP_400_BAD_REQUEST
        )

    country = form.cleaned_data.get("country")
    city = form.cleaned_data.get("city")
    gender = form.cleaned_data.get("gender")
    hair = form.cleaned_data.get("hair")
    eyes = form.cleaned_data.get("eyes")
    height = form.cleaned_data.get("height")

    # data is 1.40-1.60
    # split to get each one
    height = height.split("-")

    start = 0
    count = 20

    # Get the data
    fields = (
        "image",
        "profile__first_name",
        "profile__last_name",
        "profile__country",
        "profile__city",
    )

    models = (
        ProfilePicture.objects.filter(
            inUse=True,
            user__is_public=True,
            profile__country__iexact=country,
            profile__city__iexact=city,
            profile__gender__iexact=gender,
            user__mensuration__hair__iexact=hair,
            user__mensuration__eyes__iexact=eyes,
            user__mensuration__height__gte=height[0],
            user__mensuration__height__lte=height[1],
        ).select_related('profile')
        .only(*fields)
        .order_by("-user__created_at")[start:count]
    )

    context = {"data": models, "form": form}
    return render(request, "models/search.html", context)
