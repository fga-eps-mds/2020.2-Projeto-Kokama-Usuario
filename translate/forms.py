from django import forms
from django.forms import formset_factory
from django.core.validators import RegexValidator
# from .models import Bird

class PhraseForm(forms.Form):
    phrase_kokama = forms.RegexField(
        label='', 
        regex='.*<.+>.*',
        error_messages={'invalid': ("A frase deve conter uma palavra destacada com <>. Ex: <panara>.")},
    )
    
    phrase_portuguese = forms.RegexField(
        label='', 
        regex='.*<.+>.*',
        error_messages={'invalid': ("A frase deve conter uma palavra destacada com <>. Ex: <banana>.")},
    )

class WordKokamaForm(forms.Form):
    word_kokama = forms.CharField(
        label='',
        error_messages={'required': 'Preencha este campo.'}
    )

class WordPortugueseForm(forms.Form):
    word_portuguese = forms.CharField(
         label='',
         error_messages={'required': 'Preencha este campo.'}
    )

class PronunciationChoisesForm(forms.Form):
    pronunciation_choises = forms.ChoiceField(
        choices = (
            ("1", "Geral"),
            ("2", "Feminino"),
            ("3", "Masculino"),
        ),
        label='',
    )

PhraseFormSet = formset_factory(
    PhraseForm, 
    extra = 1
)

WordPortugueseFormSet = formset_factory(
    WordPortugueseForm, 
    extra = 1
)

