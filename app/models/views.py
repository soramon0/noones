from django.shortcuts import render
from .models import Model, Mensuration, Photo
from pages.forms import SearchForm


def models(request):
    models = Model.objects.all()

    context = {
        'models': models,
        'form': SearchForm()
    }

    return render(request, 'models/index.html', context)


def model(request, id):
    model = Model.objects.get(pk=id)

    context = {
        'model': model,
        'mensures': [],
        'photos': [],
    }

    try:
        photos = Photo.objects.filter(model_id=model.id)
        mensures = Mensuration.objects.filter(model_id=model.id)[0]
        context['mensures'] = mensures
        context['photos'] = photos
    except Photo.DoesNotExist:
        return render(request, 'models/model.html', context)

    return render(request, 'models/model.html', context)
