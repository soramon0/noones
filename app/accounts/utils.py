from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from models.models import Model, History, Mensuration

User = get_user_model()
email_txt = get_template('accounts/activate_email.txt')
email_html = get_template('accounts/activate_email.html')


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(
            microsecond=0, tzinfo=None)
        return str(user.pk) + str(user.is_active) + str(login_timestamp) + str(timestamp)


generate_token = TokenGenerator()


def send_verification_email(request, user):
    # Setup for email verfication link
    current_site = get_current_site(request)
    email_subject = 'Activate Your Account'
    context = {
        'user': user,
        'domain': current_site.domain,
        'protocol': request.scheme,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    }

    text_content = email_txt.render(context)
    html_content = email_html.render(context)

    email = EmailMultiAlternatives(
        email_subject,
        text_content,
        settings.EMAIL_HOST_USER,
        (user.email,)
    )

    email.attach_alternative(html_content, 'text/html')

    email.send()


def create_user(data):
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    birth_date = data.get('birth_date')
    facebook = data.get('facebook')
    instagram = data.get('instagram')
    phone = data.get('phone')
    addresse = data.get('addresse')
    # TODO(karim): convert to lower case
    city = data.get('city')
    country = data.get('country')
    zipcode = data.get('zipcode')
    cin = data.get('cin')
    sexe = data.get('sexe')
    handle = f'{first_name.replace(" ", "-")}-{last_name.replace(" ", "-")}'
    q1 = data.get('q1')
    q2 = data.get('q2')
    q3 = data.get('q3')
    q4 = data.get('q4')
    taille = data.get('taille')
    taillenombrill = data.get('taillenombrill')
    buste = data.get('buste')
    epaules = data.get('epaules')
    hanches = data.get('hanches')
    poids = data.get('poids')
    pointure = data.get('pointure')
    cheveux = data.get('cheveux')
    yeux = data.get('yeux')
    permitted = data.get('permitted')

    user = User.objects.create_user(email=email, password=password)

    history = History.objects.create(q1=q1, q2=q2, q3=q3, q4=q4, user=user)

    measures = Mensuration.objects.create(taille=taille, taillenombrill=taillenombrill, buste=buste, epaules=epaules,
                                          hanches=hanches, poids=poids, pointure=pointure, cheveux=cheveux, yeux=yeux,
                                          permitted=permitted, user=user)

    model = Model.objects.create(first_name=first_name, last_name=last_name, handle=handle, birth_date=birth_date, facebook=facebook,
                                 instagram=instagram, phone=phone, addresse=addresse, city=city, country=country, zipcode=zipcode,
                                 cin=cin, sexe=sexe, history_id=history.id, measures=measures, user=user)

    return (user, model, history, measures)
