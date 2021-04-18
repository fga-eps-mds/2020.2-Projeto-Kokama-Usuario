from django import forms
from django.core.validators import RegexValidator


class StoryForm(forms.Form):

    title = forms.CharField(
        label='title',
        error_messages={'required': 'Preencha este campo.'}
    )
    
    text = forms.CharField(
        label='text',
        widget=forms.Textarea,
        error_messages={'required': 'Preencha este campo.'}
    )
   