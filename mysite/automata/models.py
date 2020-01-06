from django import forms

# Create your models here.

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your automaton in json')
