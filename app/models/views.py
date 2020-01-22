from django.shortcuts import render
from .models import Model


def models(request):
    models = Model.objects.all()

    context = {
        'models': models,
    }

    return render(request, 'models/index.html', context)
