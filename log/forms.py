from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Companies, Comments

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Login", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Hasło", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class CompanyForm(forms.ModelForm):

    class Meta:
        model = Companies
        fields = ('name', 'nip', 'phone', 'st_address', 'city')

class CommentForm(forms.ModelForm):
    title = forms.CharField(max_length=80, label='Tytuł', widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'title', 'required': 'required'}))
    text = forms.CharField(label='Treść', widget=forms.Textarea(attrs={'class': 'form-control', 'name': 'text', 'required': 'required'}))
    class Meta:
        model = Comments
        fields = ('title', 'text')

class LookforForm(forms.Form):
    keyword = forms.CharField(label='keyword', max_length=70, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'keyword'}))

    def get_keyword(self):
        return self.keyword

class PdfFilesForm(forms.Form):
    companypdf = forms.FileField(
        label='Wybierz plik do zuploadowania',
        help_text='maksymalnie 100Mb',
        required='required',
    )
