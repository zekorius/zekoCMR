from django.contrib.auth.forms import AuthenticationForm
from django import forms
from colorful.fields import RGBColorField
from .models import Categories

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ('name', 'color')
