# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

##############################################################################

class SignupForm(UserCreationForm):
    '''class to extend built-in signup form'''

    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserFormDelete(forms.Form):
    '''class to define fields of user delete form'''

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
