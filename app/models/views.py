from django.shortcuts import render, get_object_or_404

from pages.forms import SearchForm
from models.forms import ModelContactForm
from models.models import (
    Model,
    Mensuration,
    Photo,
    Contact,
    ProfilePicture,
    CoverPicture,
)


def list_models(request):
    models = ProfilePicture.objects.filter(
        inUse=True, model__is_public=True).order_by('-model__created_at')[:20]
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
