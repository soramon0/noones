from django import forms

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
    pays = forms.ChoiceField(choices=(
        ('maroc', 'Maroc'),
        ('france', 'France'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
    ville = forms.ChoiceField(choices=(
        ('marrakech', 'Marrakech'),
        ('agadir', 'Agadir'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
    sexe = forms.ChoiceField(choices=(
        ('f', 'Femme'),
        ('f', 'Homme'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
    cheveux = forms.ChoiceField(choices=(
        ('brown', 'Brown'),
        ('yellow', 'Yellow'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
    yeux = forms.ChoiceField(choices=(
        ('yellow', 'Yellow'),
        ('brown', 'Brown'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
    taille = forms.ChoiceField(choices=(
        ('1.40-1.60', '1.40-1.60'),
        ('1.60-1.80', '1.60-1.80'),
        ('1.80-2.00', '1.80-2.00'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
