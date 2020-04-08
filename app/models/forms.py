from django.forms import ModelForm as MForm, TextInput, Textarea, Select, NumberInput, URLInput
from django import forms

from core.models import User
from .models import Model, History, Mensuration

INPUT_CLASS = {'class': 'form-input'}
TEXTAREA_CLASS = {'class': 'form-textarea'}
SELECT_CLASS = {'class': 'form-select'}
RADIO_CLASS = {'class': 'form-radio'}
CHECKBOX_CLASS = {'class': 'form-checkbox'}
HIDDEN_CLASS = {'class': 'form-input hidden'}
INPUT_CLASS_DISABLED = {'class': 'form-input', 'disabled': 'true'}


class UserForm(MForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs=INPUT_CLASS),
            'password': forms.PasswordInput(attrs=INPUT_CLASS)
        }


class ModelForm(MForm):
    class Meta:
        model = Model
        fields = ['sexe', 'first_name', 'last_name', 'bio', 'birth_date',
                  'facebook', 'instagram', 'phone', 'addresse', 'city', 'country', 'zipcode', 'cin']
        widgets = {
            'first_name': TextInput(attrs=INPUT_CLASS),
            'last_name': TextInput(attrs=INPUT_CLASS),
            'birth_date': forms.DateInput(attrs=INPUT_CLASS),
            'facebook': URLInput(attrs=INPUT_CLASS),
            'instagram': URLInput(attrs=INPUT_CLASS),
            'phone': TextInput(attrs=INPUT_CLASS),
            'addresse': TextInput(attrs=INPUT_CLASS),
            'country': TextInput(attrs=INPUT_CLASS),
            'city': TextInput(attrs=INPUT_CLASS),
            'zipcode': TextInput(attrs=INPUT_CLASS),
            'cin': TextInput(attrs=INPUT_CLASS),
            'sexe': Select(attrs=SELECT_CLASS),
        }


class HistoryForm(MForm):
    class Meta:
        model = History
        fields = ['q1', 'q2', 'q3', 'q4']
        widgets = {
            'q1': Textarea(attrs=TEXTAREA_CLASS),
            'q2': Textarea(attrs=TEXTAREA_CLASS),
            'q3': Textarea(attrs=TEXTAREA_CLASS),
            'q4': forms.RadioSelect(attrs=RADIO_CLASS),
        }


class MensurationForm(MForm):
    class Meta:
        model = Mensuration
        fields = ['taille', 'taillenombrill', 'buste', 'epaules',
                  'hanches', 'poids', 'pointure', 'cheveux', 'yeux', 'permitted']
        widgets = {
            'taille': NumberInput(attrs=INPUT_CLASS),
            'taillenombrill': NumberInput(attrs=INPUT_CLASS),
            'buste': NumberInput(attrs=INPUT_CLASS),
            'epaules': NumberInput(attrs=INPUT_CLASS),
            'hanches': NumberInput(attrs=INPUT_CLASS),
            'poids': NumberInput(attrs=INPUT_CLASS),
            'pointure': NumberInput(attrs=INPUT_CLASS),
            'cheveux': Select(attrs=SELECT_CLASS),
            'yeux': Select(attrs=SELECT_CLASS),
            'permitted': forms.CheckboxInput(attrs=CHECKBOX_CLASS),
        }


class ModelContactForm(forms.Form):
    model_id = forms.CharField(
        max_length=100, widget=TextInput(attrs=HIDDEN_CLASS))
    model_nom = forms.CharField(
        min_length=3, max_length=100, widget=TextInput(attrs=INPUT_CLASS_DISABLED))
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=INPUT_CLASS))
    phone = forms.CharField(min_length=6, max_length=100,
                            widget=TextInput(attrs=INPUT_CLASS))
