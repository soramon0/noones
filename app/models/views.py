from django.shortcuts import render


def models(request):
    return render(request, 'models/index.html')
