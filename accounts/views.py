from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.views.generic import View
from django.utils.translation import gettext as _
from rest_framework import status

from models.forms import ProfileForm, MensurationForm, HistoryForm
from accounts.forms import SigninForm
from accounts.services import user_create, user_activate, confirmation_email_send


User = auth.get_user_model()


def profile(request):
    if not request.user.is_authenticated:
        return render(request, "accounts/signin.html", {"form": SigninForm()})

    if request.user.is_superuser:
        return redirect("index")

    try:
        # Handling when admin user logs in
        # admin does't have the requried fields for this page
        # So we redirect him
        # TODO(karim): handle the navigation to not include a link to this page
        # TODO(karim): use this in the view
        profile = request.user.profile
    except User.profile.RelatedObjectDoesNotExist:
        return redirect("index")

    return render(request, "accounts/profile.html", {"profile": profile})


def signin(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = SigninForm(request.POST)

        if not form.is_valid():
            return render(request, "accounts/signin.html", {"form": form})

        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        invalid_message = "Invalid credentials."

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, invalid_message)
            return render(request, "accounts/signin.html", {"form": form})

        if not user.check_password(password):
            messages.error(request, invalid_message)
            return render(request, "accounts/signin.html", {"form": form})

        if not user.is_active:
            confirmation_message = (
                "You need to confirm your email before you can sign in."
            )
            messages.error(request, confirmation_message)
            return render(request, "accounts/signin.html", {"form": form})

        auth.login(request, user)

        return redirect("profile")

    return render(request, "accounts/signin.html", {"form": SigninForm()})


def signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect("index")
    return redirect("index")


def signup(request):
    # TODO(karim): handle which step to show when errors occure
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        profile_form = ProfileForm(request.POST)
        history_form = HistoryForm(request.POST)
        measures_form = MensurationForm(request.POST)

        profile_form_valid = profile_form.is_valid()
        history_form_valid = history_form.is_valid()
        measures_form_valid = measures_form.is_valid()
        context = {
            "profile_form": profile_form,
            "history_form": history_form,
            "measures_form": measures_form,
            "step": None,
        }

        if not measures_form_valid:
            context["step"] = 3

        if not history_form_valid:
            context["step"] = 2

        if not profile_form_valid:
            context["step"] = 1

        if context.get("step") is not None:
            return render(request, "accounts/register.html", context)

        email = profile_form.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            messages.error(request, _("Email provided is already in use."))
            context['step'] = 1
            return render(request, "accounts/register.html", context)

        # if any of this dicts have same keys
        # they will overwrite each other
        data = {
            **profile_form.cleaned_data,
            **history_form.cleaned_data,
            **measures_form.cleaned_data,
        }

        user, *__ = user_create(data=data)

        confirmation_email_send(request=request, user=user)

        messages.success(
            request, "Please Confirm your email to complete registration.")

        return redirect("signin")

    context = {
        "profile_form": ProfileForm(),
        "history_form": HistoryForm(),
        "measures_form": MensurationForm(),
        "step": 1,
    }

    return render(request, "accounts/register.html", context)


def activate_account(request, uidb64, token):
    if user_activate(uidb64=uidb64, token=token):
        messages.success(request, "Account activated Successfully.")
        return redirect("signin")

    return render(
        request, "accounts/activate_failed.html", status=status.HTTP_401_UNAUTHORIZED
    )
