from django.shortcuts import render
from core.models import User
from models.models import Model
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

        if User.objects.filter(email=email).exists():
            print('exists')

        user = User.objects.create_user(email=email, password=password)

        model = Model(first_name=first_name, last_name=last_name, handle=handle, birth_date=birth_date, facebook=facebook,
                      instagram=instagram, phone=phone, addresse=addresse, city=city, country=country, zipcode=zipcode,
                      cin=cin, sexe=sexe)

        model.user_id = user.id

        model.save()

        return render(request, 'accounts/register.html')

    else:
        context = {
            'form': RegisterForm()
        }
        return render(request, 'accounts/register.html', context)
