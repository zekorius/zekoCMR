from django import forms
from django.contrib.auth.models import User
from .models import Message

class MessageForm(forms.ModelForm):
    title = forms.CharField(max_length=60, label='Tytuł', widget=forms.TextInput(attrs={'placeholder':'Tytuł komentarza', 'required':'required'}))
    text = forms.CharField(label='Treść', widget=forms.Textarea(attrs={'required':'required',}) )
    class Meta:
        model = Message
        fields = ('title', 'text')
    #mssg_from = forms.ForeignKey(default = 1, related_name = 'message_from')
    #mssg_to = forms.ForeignKey(default = 1, related_name = 'message_to')
