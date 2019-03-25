# forms.py

from django import forms
from django.core.exceptions import ValidationError

import base.forms as valid
from .models import Film, Comment

##############################################################################

class FilmForm(forms.Form):
    '''class to define fields and validations of film form'''

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    title = valid.CharFieldNotBlank(required=False, max_length=100)
    year = forms.CharField(required=False, max_length=4, validators=[valid.isDigit(), valid.inLength(4, 4), valid.inRange('1900', '2100')])
    summary = forms.CharField(required=False, max_length=1000, widget=forms.Textarea())
    image_from_url = forms.CharField(required=False, max_length=1000, validators=[valid.url()])
    image_from_file = forms.ImageField(required=False, validators=[valid.sizeLimit()])
    remove_image = forms.BooleanField(required=False)

    def clean_title(self):
        found=Film.objects.filter(title=self.cleaned_data['title'].strip()).first()
        if found and found.id!=self.cleaned_data['id']: 
            raise ValidationError('Already exists')
        return self.cleaned_data['title'].strip()


class FilmFormDelete(forms.Form):
    '''class to define fields of film delete form'''

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())


class CommentForm(forms.Form):
    '''class to define fields and validations of comment form'''
    
    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    film_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    comment = valid.CharFieldNotBlank(required=False, max_length=1000, widget=forms.Textarea())


class CommentFormDelete(forms.Form):
    '''class to define fields (no validations) of comment delete form'''

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    film_id = forms.IntegerField(widget=forms.HiddenInput())
    comment = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(), disabled=True)