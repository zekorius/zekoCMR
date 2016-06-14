from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Companies

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Login", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Hasło", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Companies
        fields = ('name', 'nip',)

