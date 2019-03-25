# forms.py

from django.forms import CharField
from django.core.exceptions import ValidationError
from urllib import request


class CharFieldNotBlank(CharField):
    '''class to validate field value as not blank'''

    def to_python(self, value):
        value=value.strip()
        if not value: raise ValidationError('Required.')
        return value


def notBlank(msg=None):
    '''function to validate field value as not blank'''

    if not msg: msg='Required.'
    def _(value):
        if not value or value.strip()=='empty': raise ValidationError(msg)
    return _


def isDigit(msg=None):
    '''function to validate field value as digits only'''

    if not msg: msg='Only digits.'
    def _(value):
        if not value.isdigit(): raise ValidationError(msg)
    return _


def inLength(start=None, end=None, msg=None):
    '''function to validate field value in allowed length'''

    if not msg: msg='Length '+(str(start) if start else '')+('-'+str(end) if end and end>start else '')+'.'
    def _(value):
        if not value: pass
        elif start is not None and len(value)<start: raise ValidationError(msg)
        elif end is not None and len(value)>end: raise ValidationError(msg)
    return _


def inRange(start=None, end=None, msg=None):
    '''function to validate field value in allowed range'''

    if not msg: msg='Range '+(str(start) if start else '')+'-'+(str(end) if end else '')+'.'
    def _(value):
        if not value: pass
        elif start is not None and value<start: raise ValidationError(msg)
        elif end is not None and value>end: raise ValidationError(msg)
    return _


def sizeLimit(limit=int(2.5*1024*1024), msg=None):
    '''function to validate file field value within allowed size limit'''

    if not msg: msg='Size limit '+str(limit)+' bytes.'
    def _(value):
        if not value: pass
        elif value.size>limit: raise ValidationError(msg)
    return _


def url():
    '''function to validate field value as url'''
    
    def _(value):
        types = '.jpg .jpeg .bmp .gif .png .svg .ico '
        if not value: pass
        elif '.' + value.split('.')[-1] + ' ' not in types:
            raise ValidationError('Acceptable images: '+types)
        else:
            try: handler = request.urlopen(value)
            except Exception as e: raise ValidationError(e)
    return _