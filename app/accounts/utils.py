from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(
            microsecond=0, tzinfo=None)
        return str(user.pk) + str(user.is_active) + str(login_timestamp) + str(timestamp)


generate_token = TokenGenerator()


email_txt = get_template('accounts/activate_email.txt')
email_html = get_template('accounts/activate_email.html')


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
        [user.email]
    )

    email.attach_alternative(html_content, 'text/html')

    email.send()
