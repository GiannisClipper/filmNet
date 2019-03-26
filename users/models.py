#from django.db import models
from django.contrib.auth.models import User as User_builtin
from django.urls import reverse
import os

class User(User_builtin):
    '''class extending User built-in model'''

    class Meta:
        proxy = True

    def get_delete_url(self):
        return reverse('user-delete', args=[str(self.id)])
