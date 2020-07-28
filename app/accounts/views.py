from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views.generic import View
from rest_framework import status

from models.models import Model, Mensuration, History
from accounts.forms import RegisterForm, SigninForm
from accounts.utils import send_verification_email, generate_token


User = auth.get_user_model()


def profile(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/signin.html', {'form': SigninForm()})
    return render(request, 'accounts/profile.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = SigninForm(request.POST)

        if not form.is_valid():
            return render(request, 'accounts/signin.html', {'form': form})

        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        invalid_message = 'Invalid credentials.'

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, invalid_message)
            return render(request, 'accounts/signin.html', {'form': form})

        if not user.check_password(password):
            messages.error(request, invalid_message)
            return render(request, 'accounts/signin.html', {'form': form})

        if not user.is_active:
            confirmation_message = 'You need to confirm your email before you can sign in.'
            messages.error(request, confirmation_message)
            return render(request, 'accounts/signin.html', {'form': form})

        auth.login(request, user)

        return redirect('profile')

    return render(request, 'accounts/signin.html', {'form': SigninForm()})


def signout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('index')
    return redirect('index')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, 'accounts/register.html', {'form': form})

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        birth_date = form.cleaned_data['birth_date']
        facebook = form.cleaned_data['facebook']
        instagram = form.cleaned_data['instagram']
        phone = form.cleaned_data['phone']
        addresse = form.cleaned_data['addresse']
        # TODO(karim): convert to lower case
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']
        zipcode = form.cleaned_data['zipcode']
        cin = form.cleaned_data['cin']
        sexe = form.cleaned_data['sexe']
        handle = f'{first_name.replace(" ", "-")}-{last_name.replace(" ", "-")}'
        q1 = form.cleaned_data['q1']
        q2 = form.cleaned_data['q2']
        q3 = form.cleaned_data['q3']
        q4 = form.cleaned_data['q4']
        taille = form.cleaned_data['taille']
        taillenombrill = form.cleaned_data['taillenombrill']
        buste = form.cleaned_data['buste']
        epaules = form.cleaned_data['epaules']
        hanches = form.cleaned_data['hanches']
        poids = form.cleaned_data['poids']
        pointure = form.cleaned_data['pointure']
        cheveux = form.cleaned_data['cheveux']
        yeux = form.cleaned_data['yeux']
        permitted = form.cleaned_data['permitted']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email provided is already in use.')
            return render(request, 'accounts/register.html', {'form': form})

        user = User.objects.create_user(email=email, password=password)

        history = History.objects.create(q1=q1, q2=q2, q3=q3, q4=q4, user=user)

        measures = Mensuration.objects.create(taille=taille, taillenombrill=taillenombrill, buste=buste, epaules=epaules,
                                              hanches=hanches, poids=poids, pointure=pointure, cheveux=cheveux, yeux=yeux,
                                              permitted=permitted, user=user)

        model = Model.objects.create(first_name=first_name, last_name=last_name, handle=handle, birth_date=birth_date, facebook=facebook,
                                     instagram=instagram, phone=phone, addresse=addresse, city=city, country=country, zipcode=zipcode,
                                     cin=cin, sexe=sexe, history_id=history.id, measures=measures, user=user)

        send_verification_email(request, user)

        messages.success(
            request, 'Please Confirm your email to complete registration.')

        return redirect('signin')

    return render(request, 'accounts/register.html', {'form': RegisterForm()})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        # ex can be:
        # (DjangoUnicodeDecodeError, User.DoesNotExist, ValueError, TypeError, OverflowError, ValidationError)
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated Successfully.')
        return redirect('signin')

    return render(request, 'accounts/activate_failed.html', status=status.HTTP_401_UNAUTHORIZED)
