from django import forms


class StoryForm(forms.Form):

    title_portuguese = forms.CharField(
        label='title',
        required=False,
        error_messages={'required': 'Preencha este campo.'}
    )
    
    text_portuguese = forms.CharField(
        label='text',
        required=False,
        widget=forms.Textarea,
        error_messages={'required': 'Preencha este campo.'}
    )

    title_kokama = forms.CharField(
        label='title',
        required=False,
        error_messages={'required': 'Preencha este campo.'}
    )
    
    text_kokama = forms.CharField(
        label='text',
        required=False,
        widget=forms.Textarea,
        error_messages={'required': 'Preencha este campo.'}
    )
   