from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.http.request import RawPostDataException
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.conf import settings

from pages.forms import SearchForm
from .forms import ModelContactForm
from .models import Model, Mensuration, Photo, Contact
import json


def models(request):
    # TODO(karim): check for is_public
    models = Model.objects.all()[:12]

    context = {
        'models': models,
        'form': SearchForm()
    }

    return render(request, 'models/index.html', context)


def model(request, id):
    model = Model.objects.get(pk=id)

    context = {
        'model': model,
        'mensures': model.measures,
        'photos': [],
        'form': ModelContactForm(initial={
            'model_id': model.id,
            'model_nom': f'{model.first_name} {model.last_name}',
        })
    }

    try:
        photos = Photo.objects.filter(model_id=model.id)
        context['photos'] = photos
    except Photo.DoesNotExist:
        return render(request, 'models/model.html', context)

    return render(request, 'models/model.html', context)


def contact(request):
    if request.method == 'POST':
        # TODO(karim): check if this the right exception
        try:
            data = json.loads(request.body.decode('utf-8'))
        except RawPostDataException:
            return JsonResponse({'errors': { 'json': ['data is not valid json'] }})

        form = ModelContactForm(data)
        
        if not form.is_valid():
            context = {
                'errors': form.errors,
            }
            return JsonResponse(context)

        model_id = form.cleaned_data.get('model_id')
        model_nom = form.cleaned_data.get('model_nom')
        email = form.cleaned_data.get('email')
        phone = form.cleaned_data.get('phone')

        error = {'errors': { 'model_nom': ['model do not exist'] }}

        try:
            model = Model.objects.get(pk=model_id)
            model_email = model.user.email
        except Model.DoesNotExist:
            return JsonResponse(error)
        except ValidationError:
            return JsonResponse(error)

        send_mail(
            f'Contact Request for {model_email}',
            f'Client {email} {phone} wants to contact {model_email}',
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # TODO(karim): Send email to admin
        contact = Contact(model_id=model_id, model_nom=model_nom, model_email=model_email, email=email, phone=phone)
        contact.save()

        return JsonResponse({'message': 'Contact ws successful'})


def subset(request):
    try:
        start = int(request.GET.get('start', 0))
        count = int(request.GET.get('count', 12))
    except ValueError:
        start = 0
        count = 12
    
    # TODO(karim): check for is_public
    models = serialize('json', Model.objects.all()[start:count])

    return JsonResponse({'models': models})

def search(request):
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
    taille = taille.split('-')

    models = Model.objects.filter(
        country__iexact=pays, city__iexact=ville, sexe__iexact=sexe,
        measures__cheveux__iexact=cheveux, measures__yeux__iexact=yeux,
        measures__taille__gte=taille[0], measures__taille__lte=taille[1],
    )

    context = {
        'models': models,
        'form': form
    }
    return render(request, 'models/search.html', context)