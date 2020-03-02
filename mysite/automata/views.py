
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from Autom import automata as aut
from django import forms
from django.db import models
import json
import logging

from django.http import HttpResponseRedirect


class InputAutomata(forms.Form):
    text = forms.CharField(label='Post:', max_length=2000, 
                                   widget=forms.Textarea(attrs={'rows':'10', 'cols': '50'}))
    file = forms.FileField()

class InputWord(forms.Form):
    word = forms.CharField()


def result(request):
    text = request.POST["word"]
    defin = request.POST["automata"]
    a = aut.Automaton()
    a.definition = json.loads(defin)
    correct = a.iterate_text(text):
    return Automata(request, False, True, True, json.dumps(a.definition), correct)

def index(request):
    a = "something"
    return render(request, 'automata/result.html', {"automaton_result" : a})

def Automata(request, error=False, AutomatonParsed=False, hasAutomaton=False, automat=None, result=None, word=""):
    inputAutomata = InputAutomata()
    inputWord = InputWord()
    if 'error' in request.GET:
        error = True
    return render(request, 'automata/input.html', {
        'InputAutomata': inputAutomata,
        'InputWord' : inputWord,
        'error': error,
        'AutomatonParsed' : AutomatonParsed,
        'hasAutomaton' : hasAutomaton,
        'Automat' : automat,
        'result' : result,
        'word': word
           })

def createAutomatFromForm(request):
    form = InputAutomata(request.POST, request.FILES)
    au = aut.Automaton()
    if request.FILES:
        a = request.FILES['file']
        b = json.load(a)
        au.definition = b
    else:
        au.definition = json.loads(request.POST['text'])

    return Automata(request, False, True, True, json.dumps(au.definition))

def input(request):
    if request.method == 'POST':
        if "SubmitAutomaton" in request.POST:
            return createAutomatFromForm(request)
        if "SubmitWord" in request.POST: 
            return result(request)
    else:
        return Automata(request)
    #return index(request)
        

