# models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import os
import glob
from filmNet.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL

##############################################################################

class Film(models.Model):
    '''model representing a film'''

    title = models.CharField(max_length=100, unique=True)
    year = models.CharField(max_length=4, null=True)
    summary = models.TextField(max_length=1000)

    created_at = models.DateTimeField() #auto_now_add=True
    updated_at = models.DateTimeField() #auto_now=True
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['year']),
            models.Index(fields=['-updated_at']),
            models.Index(fields=['user', '-updated_at'])
        ]

    media_path = 'films/' #to store images as files inside /media/films

    def __str__(self):
        return f'{self.title} ({self.year})'

    def get_created_or_updated(self):
        return 'created' if self.created_at==self.updated_at else 'updated'

    def get_updated_at_formatted(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_update_url(self):
        return reverse('film-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('film-delete', args=[str(self.id)])

    def get_comments_url(self):
        return reverse('film-comments', args=[str(self.id)])

    def get_image_url(self):
        found = glob.glob(f'{MEDIA_ROOT}/{self.media_path}{str(self.id)}.*')
        if found: 
            found[0] = f'{MEDIA_URL}{self.media_path}{str(self.id)}.'+found[0].split('.')[-1]
        else:
            found=[f'{STATIC_URL}media/generic.jpg']
        return found[0]

    def get_comments(self):
        return Comment.objects.filter(film_id=self.id)

    def get_comments_count(self):
        return Comment.objects.filter(film_id=self.id).count()

##############################################################################

class Comment(models.Model):
    '''model representing a film comment'''

    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)

    created_at = models.DateTimeField() #auto_now_add=True
    updated_at = models.DateTimeField() #auto_now=True
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['-updated_at']),
            models.Index(fields=['user', '-updated_at'])
        ]

    def __str__(self):
        return f'{self.comment[:30]}'+'...' if len(self.comment)>30 else ''

    def get_created_or_updated(self):
        return 'created' if self.created_at==self.updated_at else 'updated'

    def get_updated_at_formatted(self):
        return self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_update_url(self):
        return reverse('comment-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('comment-delete', args=[str(self.id)])
