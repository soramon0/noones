from django import forms
from django.utils.translation import gettext_lazy as _

from models.models import GENDER_CHOICES
from models.forms import HAIR_CHOICES

INPUT_CLASS = {'class': 'form-input'}
TEXTAREA_CLASS = {'class': 'form-textarea w-full h-48'}
SELECT_CLASS = {'class': 'form-select'}


class ContactForm(forms.Form):
    nom = forms.CharField(
        min_length=3, max_length=100, widget=forms.TextInput(attrs=INPUT_CLASS))
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=INPUT_CLASS))
    phone = forms.CharField(
        min_length=6, max_length=100, widget=forms.TextInput(attrs=INPUT_CLASS))
    subject = forms.CharField(
        min_length=3, max_length=100, widget=forms.TextInput(attrs=INPUT_CLASS))
    message = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs=TEXTAREA_CLASS))


class SearchForm(forms.Form):
    # TODO(karim): transalte or get a mdae up list of countries and cities
    country = forms.ChoiceField(
        choices=(
            ('maroc', 'Maroc'),
            ('france', 'France'),
        ),
        label=_('country'),
        widget=forms.Select(attrs=SELECT_CLASS)
    )
    city = forms.ChoiceField(
        choices=(
            ('marrakech', 'Marrakech'),
            ('agadir', 'Agadir'),
        ),
        label=_('city'),
        widget=forms.Select(attrs=SELECT_CLASS)
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        label=_('gender'),
        widget=forms.Select(attrs=SELECT_CLASS)
    )
    hair = forms.ChoiceField(
        choices=HAIR_CHOICES, label=_('hair'),
        widget=forms.Select(attrs=SELECT_CLASS),
    )
    eyes = forms.ChoiceField(
        choices=HAIR_CHOICES, label=_('eyes'),
        widget=forms.Select(attrs=SELECT_CLASS)
    )
    height = forms.ChoiceField(
        choices=(
            ('1.40-1.60', '1.40-1.60'),
            ('1.60-1.80', '1.60-1.80'),
            ('1.80-2.00', '1.80-2.00'),
        ),
        label=_('height'),
        widget=forms.Select(attrs=SELECT_CLASS)
    )
