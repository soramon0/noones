from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from models.models import History, Mensuration, Profile
from accounts.utils import generate_token

User = get_user_model()
email_txt = get_template("accounts/activate_email.txt")
email_html = get_template("accounts/activate_email.html")


def user_create(*, data) -> (User, Profile, History, Mensuration):
    first_name = data.get("first_name", None)
    last_name = data.get("last_name", None)
    email = data.get("email", None)
    password = data.get("password", None)
    birth_date = data.get("birth_date", None)
    facebook = data.get("facebook", None)
    instagram = data.get("instagram", None)
    phone = data.get("phone", None)
    address = data.get("address", None)
    city = data.get("city")
    country = data.get("country", None)
    zipcode = data.get("zipcode", None)
    nin = data.get("nin", None)
    gender = data.get("gender", None)
    q1 = data.get("q1", None)
    q2 = data.get("q2", None)
    q3 = data.get("q3", None)
    q4 = data.get("q4", None)
    height = data.get("height", None)
    waist = data.get("waist", None)
    bust = data.get("bust", None)
    shoulders = data.get("shoulders", None)
    hips = data.get("hips", None)
    weight = data.get("weight", None)
    shoe_size = data.get("shoe_size", None)
    hair = data.get("hair", None)
    eyes = data.get("eyes", None)
    permitted = data.get("permitted", None)

    user = User.objects.create_user(email=email, password=password)

    history = History.objects.create(q1=q1, q2=q2, q3=q3, q4=q4, user=user)

    measures = Mensuration.objects.create(
        height=height,
        waist=waist,
        bust=bust,
        shoulders=shoulders,
        hips=hips,
        weight=weight,
        shoe_size=shoe_size,
        hair=hair,
        eyes=eyes,
        permitted=permitted,
        user=user,
    )

    model = Profile.objects.create(
        first_name=first_name,
        last_name=last_name,
        birth_date=birth_date,
        facebook=facebook,
        instagram=instagram,
        phone=phone,
        address=address,
        city=city,
        country=country,
        zipcode=zipcode,
        nin=nin,
        gender=gender,
        user=user,
    )

    return (user, model, history, measures)


def confirmation_email_send(*, request, user: User):
    # Setup for email verfication link
    current_site = get_current_site(request)
    email_subject = "Activate Your Account"
    context = {
        "user": user,
        "domain": current_site.domain,
        "protocol": request.scheme,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": generate_token.make_token(user),
    }

    text_content = email_txt.render(context)
    html_content = email_html.render(context)

    email = EmailMultiAlternatives(
        email_subject, text_content, settings.EMAIL_HOST_USER, (user.email,)
    )

    email.attach_alternative(html_content, "text/html")

    email.send()


def user_activate(*, uidb64: str, token: str) -> bool:
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
        return True
    else:
        return False
