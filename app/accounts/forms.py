from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(
        min_length=6, max_length=100, widget=forms.PasswordInput)
    first_name = forms.CharField(min_length=3, max_length=100)
    last_name = forms.CharField(min_length=3, max_length=100)
    birth_date = forms.DateField()
    facebook = forms.URLField()
    instagram = forms.URLField()
    phone = forms.CharField(min_length=9, max_length=100)
    addresse = forms.CharField(min_length=5, max_length=100)
    country = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)
    zipcode = forms.CharField(max_length=50)
    cin = forms.CharField(max_length=50)
    sexe = forms.ChoiceField(choices=(
        ('f', 'Femme'),
        ('f', 'Homme'),
    ))
