from django import forms

INPUT_CLASS = {'class': 'form-input'}
TEXTAREA_CLASS = {'class': 'form-textarea w-full h-48'}


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
