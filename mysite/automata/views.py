
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from Autom import automata as aut
from django import forms
from django.db import models
import json

from django.http import HttpResponseRedirect


class InputForm(forms.Form):
    word = forms.CharField()
    text = forms.CharField(label='Post:', max_length=2000, 
                                   widget=forms.Textarea(attrs={'rows':'10', 'cols': '50'}))

class InputAutomata(forms.Form):
    text = forms.CharField(label='Post:', max_length=2000, 
                                   widget=forms.Textarea(attrs={'rows':'10', 'cols': '50'}))

class InputWord(forms.Form):
    word = forms.CharField()


def result(request, text):
    a =text 
    return render(request, 'automata/result.html', {"automaton_result" : a})

def index(request):
    a = "something"
    return render(request, 'automata/result.html', {"automaton_result" : a})

def blankAutomata(request):
    error = False
    form = InputForm()
    if 'error' in request.GET:
        error = True
    return render(request, 'automata/input.html', {'form': form, 'error': error})


def input(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            word = cd['word']
            au = aut.Automaton()
            au.definition = json.loads(cd['text'])
            return result(request, au.iterate_text(word))
    else:
        return blankAutomata(request)
        

