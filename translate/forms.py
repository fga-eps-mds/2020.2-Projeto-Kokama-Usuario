from django import forms
from django.forms import formset_factory
from django.core.validators import RegexValidator


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

WordPortugueseFormSet = formset_factory(
    WordPortugueseForm, 
    extra = 1
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

PhraseFormSet = formset_factory(
    PhraseForm, 
    extra = 1
)
