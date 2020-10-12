from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _

from core import constants


class SigninForm(forms.Form):
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=constants.INPUT_CLASS))
    password = forms.CharField(
        min_length=6, max_length=100, strip=False, widget=forms.PasswordInput(attrs=constants.INPUT_CLASS))


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', **constants.INPUT_CLASS}))


class SetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', **constants.INPUT_CLASS}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', **constants.INPUT_CLASS}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
