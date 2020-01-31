from django.shortcuts import render
from django.contrib import messages

from core.models import Header
from .forms import ContactForm


def index(request):
    return render(request, 'pages/index.html')


def contact(request):
    # Get the header that's in use
    # And only one
    header = Header.objects.filter(inUse=True)
    if len(header):
        header = header[0]

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
