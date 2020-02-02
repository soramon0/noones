from django.shortcuts import render
from .models import Model
from pages.forms import SearchForm


def models(request):
    models = Model.objects.all()

    context = {
        'models': models,
        'form': SearchForm()
    }

    return render(request, 'models/index.html', context)


def model(request, id):
    print(id)
    return render(request, 'models/model.html')
