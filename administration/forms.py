from django import forms

from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserEmailField(forms.EmailField):
    def validate(self, value):
        super(forms.EmailField, self).validate(value)
        try:
            User.objects.get(email = value)
            raise forms.ValidationError("Email já existe")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("Email já existe")
        except User.DoesNotExist:
            pass

class UserCreationForm(UserCreationForm):
    email = UserEmailField(label=_("Email address"), required=True,
        help_text=_("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

