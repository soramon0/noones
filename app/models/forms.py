from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, URLInput
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

from core.models import User
from .models import Profile, History, Mensuration

INPUT_CLASS = {'class': 'form-input'}
TEXTAREA_CLASS = {'class': 'form-textarea'}
SELECT_CLASS = {'class': 'form-select'}
RADIO_CLASS = {'class': 'form-radio'}
CHECKBOX_CLASS = {'class': 'form-checkbox'}
HIDDEN_CLASS = {'class': 'form-input hidden'}
INPUT_CLASS_DISABLED = {'class': 'form-input', 'disabled': 'true'}
HAIR_CHOICES = (
    ('brown', _('brown')),
    ('yellow', _('yellow')),
    ('other', _('other'))
)


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs=INPUT_CLASS),
            'password': forms.PasswordInput(attrs=INPUT_CLASS)
        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'first_name', 'last_name', 'bio', 'birth_date',
                  'facebook', 'instagram', 'phone', 'address', 'city', 'country', 'zipcode', 'nin')
        widgets = {
            'first_name': TextInput(attrs=INPUT_CLASS),
            'last_name': TextInput(attrs=INPUT_CLASS),
            'birth_date': forms.DateInput(attrs=INPUT_CLASS),
            'facebook': URLInput(attrs=INPUT_CLASS),
            'instagram': URLInput(attrs=INPUT_CLASS),
            'phone': TextInput(attrs=INPUT_CLASS),
            'address': TextInput(attrs=INPUT_CLASS),
            'country': TextInput(attrs=INPUT_CLASS),
            'city': TextInput(attrs=INPUT_CLASS),
            'zipcode': TextInput(attrs=INPUT_CLASS),
            'nin': TextInput(attrs=INPUT_CLASS),
            'gender': Select(attrs=SELECT_CLASS),
        }
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=INPUT_CLASS))
    password = forms.CharField(
        min_length=6, max_length=100, strip=False, widget=forms.PasswordInput(attrs=INPUT_CLASS))

    def clean_password(self):
        password = self.cleaned_data['password']
        password_validation.validate_password(password)
        return password


class HistoryForm(ModelForm):
    class Meta:
        model = History
        fields = ('q1', 'q2', 'q3', 'q4')
        widgets = {
            'q1': Textarea(attrs=TEXTAREA_CLASS),
            'q2': Textarea(attrs=TEXTAREA_CLASS),
            'q3': Textarea(attrs=TEXTAREA_CLASS),
            'q4': forms.RadioSelect(attrs=RADIO_CLASS),
        }


class MensurationForm(ModelForm):
    class Meta:
        model = Mensuration
        fields = ('height', 'waist', 'bust', 'shoulders',
                  'hips', 'weight', 'shoe_size', 'permitted')
        widgets = {
            'height': NumberInput(attrs=INPUT_CLASS),
            'waist': NumberInput(attrs=INPUT_CLASS),
            'bust': NumberInput(attrs=INPUT_CLASS),
            'shoulders': NumberInput(attrs=INPUT_CLASS),
            'hips': NumberInput(attrs=INPUT_CLASS),
            'weight': NumberInput(attrs=INPUT_CLASS),
            'shoe_size': NumberInput(attrs=INPUT_CLASS),
            'permitted': forms.CheckboxInput(attrs=CHECKBOX_CLASS),
        }
    hair = forms.ChoiceField(choices=HAIR_CHOICES, help_text=_(
        'Hair color'), widget=forms.Select(attrs=SELECT_CLASS))
    eyes = forms.ChoiceField(choices=HAIR_CHOICES, help_text=_(
        'Eye color'), widget=forms.Select(attrs=SELECT_CLASS))

    labels = {
        'hair': _('hair'),
        'eyes': _('eyes')
    }


class ModelContactForm(forms.Form):
    model_id = forms.CharField(
        max_length=100,
        widget=TextInput(attrs=HIDDEN_CLASS)
    )
    model_full_name = forms.CharField(
        min_length=3,
        max_length=100,
        widget=TextInput(attrs=INPUT_CLASS_DISABLED),
        label=_('Model Full Name')
    )
    full_name = forms.CharField(
        min_length=6,
        max_length=100,
        widget=TextInput(attrs=INPUT_CLASS),
        label=_('Your Full Name')
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs=INPUT_CLASS),
        label=_('Your Email')
    )
    phone = forms.CharField(
        min_length=6,
        max_length=100,
        widget=TextInput(attrs=INPUT_CLASS),
        label=_('Your Phone')
    )
