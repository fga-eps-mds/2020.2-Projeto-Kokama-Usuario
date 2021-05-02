from django import forms

REQUIRED_MESSAGE = 'Preencha este campo.'

class StoryForm(forms.Form):

    title_portuguese = forms.CharField(
        label='title',
        required=False,
        error_messages={'required': REQUIRED_MESSAGE}
    )
    
    text_portuguese = forms.CharField(
        label='text',
        required=False,
        widget=forms.Textarea,
        error_messages={'required': REQUIRED_MESSAGE}
    )

    title_kokama = forms.CharField(
        label='title',
        required=False,
        error_messages={'required': REQUIRED_MESSAGE}
    )
    
    text_kokama = forms.CharField(
        label='text',
        required=False,
        widget=forms.Textarea,
        error_messages={'required': REQUIRED_MESSAGE}
    )
   