from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, URLInput
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from core import constants
from core.models import User, Country
from models.models import Profile, History, Mensuration


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs=constants.INPUT_CLASS),
            'password': forms.PasswordInput(attrs=constants.INPUT_CLASS)
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'first_name', 'last_name', 'bio', 'birth_date',
                  'facebook', 'instagram', 'phone', 'address', 'city', 'country', 'zipcode', 'nin')
        widgets = {
            'first_name': TextInput(attrs=constants.INPUT_CLASS),
            'last_name': TextInput(attrs=constants.INPUT_CLASS),
            'birth_date': forms.DateInput(attrs=constants.INPUT_CLASS),
            'facebook': URLInput(attrs=constants.INPUT_CLASS),
            'instagram': URLInput(attrs=constants.INPUT_CLASS),
            'phone': TextInput(attrs=constants.INPUT_CLASS),
            'address': TextInput(attrs=constants.INPUT_CLASS),
            'city': Select(attrs=constants.SELECT_CLASS),
            'zipcode': TextInput(attrs=constants.INPUT_CLASS),
            'nin': TextInput(attrs=constants.INPUT_CLASS),
            'gender': Select(attrs=constants.SELECT_CLASS),
        }
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        widget=Select(attrs=constants.SELECT_CLASS),
        empty_label='Select a Country',
        to_field_name='code')
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=constants.INPUT_CLASS))
    password = forms.CharField(
        min_length=6, max_length=100, strip=False, widget=forms.PasswordInput(attrs=constants.INPUT_CLASS))

    def clean_password(self):
        password = self.cleaned_data['password']
        password_validation.validate_password(password)
        return password

    def clean_country(self):
        country = self.cleaned_data['country']
        if isinstance(country, Country):
            return country.name
        return country


class HistoryForm(ModelForm):
    class Meta:
        model = History
        fields = ('q1', 'q2', 'q3', 'q4')
        widgets = {
            'q1': Textarea(attrs=constants.TEXTAREA_CLASS),
            'q2': Textarea(attrs=constants.TEXTAREA_CLASS),
            'q3': Textarea(attrs=constants.TEXTAREA_CLASS),
            'q4': forms.RadioSelect(attrs=constants.RADIO_CLASS),
        }


class MensurationForm(ModelForm):
    class Meta:
        model = Mensuration
        fields = ('height', 'waist', 'bust', 'shoulders',
                  'hips', 'weight', 'shoe_size', 'permitted')
        widgets = {
            'height': NumberInput(attrs=constants.INPUT_CLASS),
            'waist': NumberInput(attrs=constants.INPUT_CLASS),
            'bust': NumberInput(attrs=constants.INPUT_CLASS),
            'shoulders': NumberInput(attrs=constants.INPUT_CLASS),
            'hips': NumberInput(attrs=constants.INPUT_CLASS),
            'weight': NumberInput(attrs=constants.INPUT_CLASS),
            'shoe_size': NumberInput(attrs=constants.INPUT_CLASS),
            'permitted': forms.CheckboxInput(attrs=constants.CHECKBOX_CLASS),
        }
    hair = forms.ChoiceField(choices=constants.HAIR_CHOICES, help_text=_(
        'Hair color'), widget=forms.Select(attrs=constants.SELECT_CLASS))
    eyes = forms.ChoiceField(choices=constants.EYES_CHOICES, help_text=_(
        'Eye color'), widget=forms.Select(attrs=constants.SELECT_CLASS))

    labels = {
        'hair': _('hair'),
        'eyes': _('eyes')
    }


class ModelContactForm(forms.Form):
    model_id = forms.CharField(
        max_length=100,
        widget=TextInput(attrs=constants.HIDDEN_CLASS)
    )
    model_full_name = forms.CharField(
        min_length=3,
        max_length=100,
        widget=TextInput(attrs=constants.INPUT_CLASS_DISABLED),
        label=_('Model Full Name')
    )
    full_name = forms.CharField(
        min_length=6,
        max_length=100,
        widget=TextInput(attrs=constants.INPUT_CLASS),
        label=_('Your Full Name')
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs=constants.INPUT_CLASS),
        label=_('Your Email'))
    phone = forms.CharField(
        min_length=6,
        max_length=100,
        widget=TextInput(attrs=constants.INPUT_CLASS),
        label=_('Your Phone')
    )
