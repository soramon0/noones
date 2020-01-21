from django.shortcuts import render
from core.models import User
from models.models import Model


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        birth_date = request.POST['birth_date']
        facebook = request.POST['facebook']
        instagram = request.POST.get('instagram')
        phone = request.POST['phone']
        addresse = request.POST['addresse']
        city = request.POST['city']
        country = request.POST['country']
        zipcode = request.POST['zipcode']
        cin = request.POST['cin']
        sexe = request.POST['sexe']

        if User.objects.filter(email=email).exists():
            print('exists')

        user = User.objects.create_user(email=email, password=password)

        model = Model(first_name=first_name, last_name=last_name, birth_date=birth_date, facebook=facebook, instagram=instagram,
                      phone=phone, addresse=addresse, city=city, country=country, zipcode=zipcode, cin=cin, sexe=sexe)

        model.user_id = user.id

        model.save()

        return render(request, 'accounts/register.html')
    else:
        return render(request, 'accounts/register.html')
