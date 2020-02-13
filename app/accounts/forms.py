from django import forms

INPUT_CLASS = {'class': 'form-input'}
TEXTAREA_CLASS = {'class': 'form-textarea'}
SELECT_CLASS = {'class': 'form-select'}
RADIO_CLASS = {'class': 'form-radio'}
CHECKBOX_CLASS = {'class': 'form-checkbox'}


class SigninForm(forms.Form):
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=INPUT_CLASS))
    password = forms.CharField(
        min_length=6, max_length=100, widget=forms.PasswordInput(attrs=INPUT_CLASS))


class RegisterForm(forms.Form):
    email = forms.EmailField(
        max_length=255, widget=forms.EmailInput(attrs=INPUT_CLASS))
    password = forms.CharField(
        min_length=6, max_length=100, widget=forms.PasswordInput(attrs=INPUT_CLASS))
    first_name = forms.CharField(
        min_length=3, max_length=100, widget=forms.TextInput(attrs=INPUT_CLASS))
    last_name = forms.CharField(min_length=3, max_length=100,
                                widget=forms.TextInput(attrs=INPUT_CLASS))
    birth_date = forms.DateField(widget=forms.DateInput(attrs=INPUT_CLASS))
    facebook = forms.URLField(
        widget=forms.URLInput(attrs=INPUT_CLASS))
    instagram = forms.URLField(
        widget=forms.URLInput(attrs=INPUT_CLASS))
    phone = forms.CharField(min_length=9, max_length=100,
                            widget=forms.TextInput(attrs=INPUT_CLASS))
    addresse = forms.CharField(min_length=5, max_length=100,
                               widget=forms.TextInput(attrs=INPUT_CLASS))
    country = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs=INPUT_CLASS))
    city = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs=INPUT_CLASS))
    zipcode = forms.CharField(max_length=50,
                              widget=forms.TextInput(attrs=INPUT_CLASS))
    cin = forms.CharField(max_length=50,
                          widget=forms.TextInput(attrs=INPUT_CLASS))
    sexe = forms.ChoiceField(choices=(
        ('f', 'Femme'),
        ('h', 'Homme'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
    q1 = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs=TEXTAREA_CLASS))
    q2 = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs=TEXTAREA_CLASS))
    q3 = forms.CharField(max_length=500, widget=forms.Textarea(
        attrs=TEXTAREA_CLASS))
    q4 = forms.ChoiceField(widget=forms.RadioSelect(attrs=RADIO_CLASS), choices=(
        ('y', 'Oui'),
        ('n', 'Non'),
    ))
    taille = forms.DecimalField(max_digits=3, decimal_places=2, widget=forms.NumberInput(attrs=INPUT_CLASS))
    taillenombrill = forms.DecimalField(max_digits=3, decimal_places=2, widget=forms.NumberInput(attrs=INPUT_CLASS))
    buste = forms.IntegerField(widget=forms.NumberInput(attrs=INPUT_CLASS))
    epaules = forms.IntegerField(widget=forms.NumberInput(attrs=INPUT_CLASS))
    hanches = forms.IntegerField(widget=forms.NumberInput(attrs=INPUT_CLASS))
    poids = forms.IntegerField(widget=forms.NumberInput(attrs=INPUT_CLASS))
    pointure = forms.IntegerField(widget=forms.NumberInput(attrs=INPUT_CLASS))
    cheveux = forms.ChoiceField(choices=(
        ('brown', 'brown'),
        ('yellow', 'yellow'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
    yeux = forms.ChoiceField(choices=(
        ('brown', 'brown'),
        ('yellow', 'yellow'),
    ), widget=forms.Select(attrs=SELECT_CLASS))
    permitted = forms.BooleanField(
        widget=forms.CheckboxInput(attrs=CHECKBOX_CLASS))
