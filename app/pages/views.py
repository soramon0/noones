from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

from core.models import Header, Carousel
from models.models import Profile, ProfilePicture
from .forms import ContactForm, SearchForm


def index(request):
    carousel = Carousel.objects.filter(inUse=True)
    # TODO(karim): check for highlight
    models = ProfilePicture.objects.filter(inUse=True, user__is_public=True).only(
        "profile", "user", "image"
    )[:12]

    context = {"carousel": carousel, "data": models, "form": SearchForm()}
    return render(request, "pages/index.html", context)


def contact(request):
    # Get the header that's in use
    # And only one
    header = Header.objects.filter(inUse=True)[:1]
    header = header[0] if len(header) else header

    if request.method == "POST":
        form = ContactForm(request.POST)

        if not form.is_valid():
            context = {"form": form, "header": header}
            return render(request, "pages/contact.html", context)

        # Send Email here
        nom = form.cleaned_data.get("nom")
        email = form.cleaned_data.get("email")
        phone = form.cleaned_data.get("phone")
        subject = form.cleaned_data.get("subject")
        message = form.cleaned_data.get("message")

        # TODO(karim): check who should get this email
        send_mail(
            f"{nom} - {phone} - {subject}",
            message,
            email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        # Set a succes message for the user
        messages.success(
            request,
            "Thank you for getting in touch! We'll get back to you as soon as possible",
        )

        # return an empty form
        context = {"form": ContactForm(), "header": header}
        return render(request, "pages/contact.html", context)

    context = {"form": ContactForm(), "header": header}

    return render(request, "pages/contact.html", context)


def apropos(request):
    return render(request, "pages/a-propos.html")


def vision(request):
    return render(request, "pages/vision.html")
