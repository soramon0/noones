from django import forms
from django.utils.translation import gettext_lazy as _

from core import constants


class ContactForm(forms.Form):
    nom = forms.CharField(min_length=3, max_length=100)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(min_length=6, max_length=100)
    subject = forms.CharField(min_length=3, max_length=100)
    message = forms.CharField(widget=forms.Textarea(
        attrs={'rows': '8', 'cols': '40'}))


class SearchForm(forms.Form):
    # TODO(karim): transalte or get a mdae up list of countries and cities
    country = forms.ChoiceField(
        choices=constants.COUNTRY_CHOICES,
        label=_('country'),
        widget=forms.Select(attrs=constants.SELECT_CLASS)
    )
    city = forms.ChoiceField(
        choices=constants.CITY_CHOICES,
        label=_('city'),
        widget=forms.Select(attrs=constants.SELECT_CLASS)
    )
    gender = forms.ChoiceField(
        choices=constants.GENDER_CHOICES,
        label=_('gender'),
        widget=forms.Select(attrs=constants.SELECT_CLASS)
    )
    hair = forms.ChoiceField(
        choices=constants.HAIR_CHOICES, label=_('hair'),
        widget=forms.Select(attrs=constants.SELECT_CLASS),
    )
    eyes = forms.ChoiceField(
        choices=constants.HAIR_CHOICES, label=_('eyes'),
        widget=forms.Select(attrs=constants.SELECT_CLASS)
    )
    height = forms.ChoiceField(
        choices=constants.HEIGHT_CHOICES,
        label=_('height'),
        widget=forms.Select(attrs=constants.SELECT_CLASS)
    )
