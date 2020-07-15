from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
import datetime
import time


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


def list_models(request):
    # TODO(karim): check for is_public
    models = ProfilePicture.objects.filter(
        inUse=True, model__is_public=False)[:20]
    context = {
        'data': models,
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

    start = 0
    count = 20

    # Get the data
    fields = ['image', 'model__first_name',
              'model__last_name', 'model__country', 'model__city']

    models = ProfilePicture.objects.filter(
        inUse=True, model__country__iexact=pays, model__city__iexact=ville,
        model__sexe__iexact=sexe, model__measures__cheveux__iexact=cheveux,
        model__measures__yeux__iexact=yeux, model__measures__taille__gte=taille[0],
        model__measures__taille__lte=taille[1]
    ).only(*fields).order_by('-model__created_at')[start:count]

    context = {
        'data': models,
        'form': form
    }
    return render(request, 'models/search.html', context)
