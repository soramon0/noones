from django import forms


class ProfileImageForm(forms.Form):
	profilePicture = forms.ImageField(upload_to='photos/%Y/%m/%d')
