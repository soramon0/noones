from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.http.request import RawPostDataException
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from pages.forms import SearchForm
from .forms import ModelContactForm
from .models import (
    Model,
    Mensuration,
    Photo,
    Contact,
    ProfilePicture,
    CoverPicture
)
import json


def list_models(request):
    # TODO(karim): check for is_public
    models = Model.objects.all()[:12]

    context = {
        'models': models,
        'form': SearchForm()
    }

    return render(request, 'models/index.html', context)


def detail_model(request, id):
    fields = ['first_name', 'last_name', 'country', 'city', 'bio', 'measures']
    queryset = Model.objects.only(*fields)
    model = get_object_or_404(queryset, pk=id)

    context = {
        'model': model,
        'measures': model.measures,
        'form': ModelContactForm(initial={
            'model_id': model.id,
            'model_full_name': f'{model.first_name} {model.last_name}',
        })
    }

    try:
        photos = Photo.objects.only('image').filter(model_id=model.id)
        context['photos'] = photos
    except Photo.DoesNotExist:
        context['photos'] = []

    try:
        profile_picture = ProfilePicture.objects.only('image').get(
            model=model.id, inUse=True)

        context['profile'] = profile_picture.image.url
    except ProfilePicture.DoesNotExist:
        context['profile'] = None

    try:
        cover_picture = CoverPicture.objects.only('image').get(
            model=model.id, inUse=True)
        context['cover'] = cover_picture.image.url
    except CoverPicture.DoesNotExist:
        context['cover'] = None

    return render(request, 'models/model.html', context)


@api_view(['POST'])
def model_contact(request):
    form = ModelContactForm(request.data)

    if not form.is_valid():
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

    model_id = form.cleaned_data.get('model_id')
    model_full_name = form.cleaned_data.get('model_full_name')
    full_name = form.cleaned_data.get('full_name')
    email = form.cleaned_data.get('email')
    phone = form.cleaned_data.get('phone')

    try:
        model = Model.objects.only('user').get(pk=model_id)
        model_email = model.user.email
    except Model.DoesNotExist:
        error = {'errors': {'model_full_name': ['model do not exist']}}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    Contact.objects.create(model=model, model_full_name=model_full_name, full_name=full_name,
                           model_email=model_email, email=email, phone=phone)

    send_mail(
        f'Contact Request for {model_email}',
        f'Client {full_name} at {email} - {phone} wants to contact {model_email}',
        email,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )

    return Response({'message': "Thanks! We'll get back to you soon."})


def model_paginated(request):
    # TODO(karim): Refactor this to use rest framework
    try:
        start = int(request.GET.get('start', 0))
        count = int(request.GET.get('count', 12))
    except ValueError:
        start = 0
        count = 12

    # TODO(karim): check for is_public
    models = serialize('json', Model.objects.all()[start:count])

    return JsonResponse({'models': models})


def model_search(request):
    form = SearchForm(request.GET)

    if not form.is_valid():
        context = {
            'form': form,
        }
        return render(request, 'models/search.html', context)

    pays = form.cleaned_data.get('pays')
    ville = form.cleaned_data.get('ville')
    sexe = form.cleaned_data.get('sexe')
    cheveux = form.cleaned_data.get('cheveux')
    yeux = form.cleaned_data.get('yeux')
    taille = form.cleaned_data.get('taille')

    # data is 1.40-1.60
    # split to get each one
    taille = taille.split('-')

    # to avoid errors down the line
    # TODO(karim): check if we should return more
    start = 0
    count = 12
    returnJson = False

    # if we do then we should return json
    # This will be true only when the client askes for more data
    if 'start' in request.GET and 'count' in request.GET:
        returnJson = True
        # If all is well, get the count
        try:
            # TODO(karim): check if we should get more on the first request
            start = int(request.GET.get('start', 0))
            count = int(request.GET.get('count', 12))
        except ValueError:
            start = 0
            count = 12

    # Get the data
    models = Model.objects.filter(
        country__iexact=pays, city__iexact=ville, sexe__iexact=sexe,
        measures__cheveux__iexact=cheveux, measures__yeux__iexact=yeux,
        measures__taille__gte=taille[0], measures__taille__lte=taille[1],
    )[start:count]

    # return json when asked by client
    if returnJson:
        return JsonResponse({'models': serialize('json', models)})

    # On the initial load return the page
    context = {
        'models': models,
        'form': form
    }
    return render(request, 'models/search.html', context)
