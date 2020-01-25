from django.shortcuts import render
from core.models import User
from django.contrib import messages

from models.models import Model, Mensuration, History
from .forms import RegisterForm


def register(request):
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

        model = Model(first_name=first_name, last_name=last_name, handle=handle, birth_date=birth_date, facebook=facebook,
                      instagram=instagram, phone=phone, addresse=addresse, city=city, country=country, zipcode=zipcode,
                      cin=cin, sexe=sexe)

        history = History(q1=q1, q2=q2, q3=q3, q4=q4)

        mensuratoin = Mensuration(
            taille=taille, taillenombrill=taillenombrill, buste=buste, epaules=epaules, hanches=hanches, poids=poids, pointure=pointure, cheveux=cheveux, yeux=yeux, permitted=permitted)

        model.user_id = user.id
        history.user_id = user.id
        mensuratoin.user_id = user.id

        model.save()
        history.save()
        mensuratoin.save()

        return render(request, 'pages/index.html')

    else:
        context = {
            'form': RegisterForm()
        }
        return render(request, 'accounts/register.html', context)
