from django import forms
from django.core.validators import RegexValidator


class StoryForm(forms.Form):

    language = forms.ChoiceField(
        choices = (
            ("1", "Ambos"),
            ("2", "Português"),
            ("3", "Kokama"),
        ),
        label='',
    )

    title = forms.CharField(
        label='title',
        error_messages={'required': 'Preencha este campo.'}
    )
    
    text = forms.CharField(
        label='text',
        widget=forms.Textarea,
        error_messages={'required': 'Preencha este campo.'}
    )
   