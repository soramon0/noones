from django.shortcuts import render
from django.contrib import messages

from core.models import Header, Carousel
from models.models import Model
from .forms import ContactForm, SearchForm


def index(request):
    carousel = Carousel.objects.filter(inUse=True)
    models = Model.objects.all()
    context = {
        'carousel': carousel,
        'models': models,
        'form': SearchForm()
    }
    return render(request, 'pages/index.html', context)


def contact(request):
    # Get the header that's in use
    # And only one
    header = Header.objects.filter(inUse=True)[:1]
    header = header[0] if len(header) else header

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if not form.is_valid():
            context = {
                'form': form,
                'header': header
            }
            return render(request, 'pages/contact.html', context)

        # Send Email here
        messages.success(
            request, 'Thank you for getting in touch! We\'ll get back to you as soon as possible')

        # return an empty form
        context = {
            'form': ContactForm(),
            'header': header
        }
        return render(request, 'pages/contact.html', context)

    context = {
        'form': ContactForm(),
        'header': header
    }

    return render(request, 'pages/contact.html', context)


def apropos(request):
    return render(request, 'pages/a-propos.html')


def vision(request):
    return render(request, 'pages/vision.html')
