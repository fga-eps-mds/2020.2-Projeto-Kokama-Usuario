from django import forms
from django.forms import formset_factory
from django.core.validators import RegexValidator
# from .models import Bird

class PhraseForm(forms.Form):
    phrase_kokama = forms.RegexField(
        label='phrase_kokama', 
        regex='.*<.+>.*',
        error_messages={'invalid': ("A frase deve conter uma palavra destacada com <>. Ex: <panara>.")},
    )
    
    phrase_portuguese = forms.RegexField(
        label='phrase_portuguese', 
        regex='.*<.+>.*',
        error_messages={'invalid': ("A frase deve conter uma palavra destacada com <>. Ex: <banana>.")},
    )

class WordKokamaForm(forms.Form):
    word_kokama = forms.CharField(
        label='word_kokama',
        error_messages={'required': 'Preencha este campo.'}
    )

class WordPortugueseForm(forms.Form):
    word_portuguese = forms.CharField(
         label='word_portuguese',
         error_messages={'required': 'Preencha este campo.'}
    )

class PronunciationChoisesForm(forms.Form):
    pronunciation_choises = forms.ChoiceField(
        choices = (
            ("1", "Geral"),
            ("2", "Feminino"),
            ("3", "Masculino"),
        ),
        label='type_pronunciation',
    )

PhraseFormSet = formset_factory(
    # Bird, fields=("common_name", "scientific_name"), extra=1
    PhraseForm, 
    extra = 1
)

WordPortugueseFormSet = formset_factory(
    WordPortugueseForm, 
    extra = 1
)

