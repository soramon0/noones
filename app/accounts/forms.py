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


class RegisterForm(forms.Form):
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=constants.INPUT_CLASS))
    password = forms.CharField(
        min_length=6, max_length=100, strip=False, widget=forms.PasswordInput(attrs=constants.INPUT_CLASS))
    first_name = forms.CharField(
        min_length=3, max_length=100, widget=forms.TextInput(attrs=constants.INPUT_CLASS))
    last_name = forms.CharField(min_length=3, max_length=100,
                                widget=forms.TextInput(attrs=constants.INPUT_CLASS))
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs=constants.INPUT_CLASS))
    facebook = forms.URLField(
        widget=forms.URLInput(attrs=constants.INPUT_CLASS))
    instagram = forms.URLField(
        widget=forms.URLInput(attrs=constants.INPUT_CLASS))
    phone = forms.CharField(min_length=9, max_length=100,
                            widget=forms.TextInput(attrs=constants.INPUT_CLASS))
    addresse = forms.CharField(min_length=5, max_length=100,
                               widget=forms.TextInput(attrs=constants.INPUT_CLASS))
    country = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs=constants.INPUT_CLASS))
    city = forms.ChoiceField(choices=constants.CITY_CHOICES,
                             widget=forms.Select(attrs=constants.SELECT_CLASS))
    zipcode = forms.CharField(max_length=50,
                              widget=forms.TextInput(attrs=constants.INPUT_CLASS))
    nin = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs=constants.INPUT_CLASS))
    gender = forms.ChoiceField(
        choices=constants.GENDER_CHOICES, widget=forms.Select(attrs=constants.SELECT_CLASS))
    q1 = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs=constants.TEXTAREA_CLASS))
    q2 = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs=constants.TEXTAREA_CLASS))
    q3 = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs=constants.TEXTAREA_CLASS))
    q4 = forms.ChoiceField(widget=forms.RadioSelect(
        attrs=constants.RADIO_CLASS), choices=constants.AGREEMENT_CHOICES)
    height = forms.DecimalField(
        max_digits=3, decimal_places=2, widget=forms.NumberInput(attrs=constants.INPUT_CLASS))
    waist = forms.DecimalField(
        max_digits=3, decimal_places=2, widget=forms.NumberInput(attrs=constants.INPUT_CLASS))
    bust = forms.IntegerField(
        widget=forms.NumberInput(attrs=constants.INPUT_CLASS))
    shoulders = forms.IntegerField(
        widget=forms.NumberInput(attrs=constants.INPUT_CLASS))
    hips = forms.IntegerField(
        widget=forms.NumberInput(attrs=constants.INPUT_CLASS))
    weight = forms.IntegerField(
        widget=forms.NumberInput(attrs=constants.INPUT_CLASS))
    show_size = forms.IntegerField(
        widget=forms.NumberInput(attrs=constants.INPUT_CLASS))
    hair = forms.ChoiceField(choices=constants.HAIR_CHOICES,
                             widget=forms.Select(attrs=constants.SELECT_CLASS))
    eyes = forms.ChoiceField(choices=constants.EYES_CHOICES,
                             widget=forms.Select(attrs=constants.SELECT_CLASS))
    permitted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs=constants.CHECKBOX_CLASS))

    def clean_password(self):
        password = self.cleaned_data['password']
        password_validation.validate_password(password)
        return password


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
