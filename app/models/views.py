from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.serializers import serialize

from pages.forms import SearchForm
from .forms import ModelContactForm
from .models import Model, Mensuration, Photo, Contact
import json
import os


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
        'mensures': [],
        'photos': [],
        'form': ModelContactForm(initial={
            'model_id': model.id,
            'model_nom': f'{model.first_name} {model.last_name}',
        })
    }

    try:
        photos = Photo.objects.filter(model_id=model.id)
        mensures = Mensuration.objects.filter(model_id=model.id)[0]
        context['mensures'] = mensures
        context['photos'] = photos
    except Photo.DoesNotExist:
        return render(request, 'models/model.html', context)

    return render(request, 'models/model.html', context)


def contact(request):
    if request.method == 'POST':
        # TODO(karim): check for exceptions 
        data = json.loads(request.body.decode('utf-8'))
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
            [os.environ.get('EMAIL_USER')],
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
    models = serialize('json',Model.objects.all()[start:count])

    return JsonResponse({'models': models})