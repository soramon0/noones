from django import forms

INPUT_CLASS = {'class': 'form-input'}
TEXTAREA_CLASS = {'class': 'form-textarea w-full h-48'}
SELECT_CLASS = {'class': 'form-select'}
HIDDEN_CLASS = {'class': 'form-input hidden'}


class ModelContactForm(forms.Form):
    model_id = forms.CharField(max_length=100, widget=forms.TextInput(attrs=HIDDEN_CLASS))
    model_nom = forms.CharField(
        min_length=3, max_length=100, widget=forms.TextInput(attrs=INPUT_CLASS))
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=INPUT_CLASS))
    phone = forms.CharField(
        min_length=6, max_length=100, widget=forms.TextInput(attrs=INPUT_CLASS))