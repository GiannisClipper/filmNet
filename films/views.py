# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from base.views import BaseView, CreateViewWithStamp, UpdateViewWithStamp, DeleteView, FileImageHandler
from base.views import BaseListWithPaginator
from .models import Film, Comment
from .forms import FilmForm, FilmFormDelete, CommentForm, CommentFormDelete

import os
from filmNet.settings import MEDIA_ROOT

##############################################################################

@login_required
def film_create(req): return FilmCreate.run(req)

@login_required
def film_update(req, id): return FilmUpdate.run(req, id)

@login_required
def film_delete(req, id): return FilmDelete.run(req, id)

def all_films(req): return AllFilms.run(req)

@login_required
def my_films(req): return MyFilms.run(req)

def film_comments(req, film_id): return FilmComments.run(req, film_id) #fullfills the need of a CommentCreate

@login_required
def comment_update(req, id): return CommentUpdate.run(req, id)

@login_required
def comment_delete(req, id): return CommentDelete.run(req, id)

def all_comments(req): return AllComments.run(req)

@login_required
def my_comments(req): return MyComments.run(req)

##############################################################################

class FilmView(BaseView):
    '''class to handle film requests'''

    Model = Film
    Form = None
    film = None
    HTMLmode = None

    @classmethod
    def not_post(cls):
        super().not_post()
        if cls.id: 
            cls.film = get_object_or_404(Film, pk=cls.id)

    @classmethod
    def save_image_from_url(cls):
        #set path and name of image file
        FileImageHandler.url_source = cls.form.cleaned_data['image_from_url']
        FileImageHandler.path = os.path.join(MEDIA_ROOT, cls.model.media_path)
        FileImageHandler.name = str(cls.model.id)
        FileImageHandler.ext = FileImageHandler.url_source.split('.')[-1]
        #delete previous image file if exist
        FileImageHandler.delete(f'{FileImageHandler.path}{FileImageHandler.name}.*')
        #save current image file
        FileImageHandler.save_from_url()
        #resize image file
        FileImageHandler.resize(width=600, height=600)

    @classmethod
    def save_image_from_file(cls):
        file = cls.req.FILES['image_from_file']
        #set path and name of image file
        FileImageHandler.file_source = file
        FileImageHandler.path = os.path.join(MEDIA_ROOT, cls.model.media_path)
        FileImageHandler.name = str(cls.model.id)
        FileImageHandler.ext = file.name.split('.')[-1]
        #delete previous image file if exist
        FileImageHandler.delete(f'{FileImageHandler.path}{FileImageHandler.name}.*')
        #save current image file
        FileImageHandler.save_from_file()
        #resize image file
        FileImageHandler.resize(width=600, height=600)

    @classmethod
    def remove_image(cls):
        FileImageHandler.path = os.path.join(MEDIA_ROOT, cls.model.media_path)
        FileImageHandler.name = str(cls.model.id)
        FileImageHandler.delete(f'{FileImageHandler.path}{FileImageHandler.name}.*')

    @classmethod
    def render(cls):
        #update & delete allowed only by user created the post
        cls.req.user.is_the_admin = True if cls.req.user.username==os.environ.get('ADMIN_USERNAME', None) else False
        if not cls.model.user or cls.model.user==cls.req.user or cls.req.user.is_the_admin:
            return render(cls.req, 'films/film_comments.html', {'form':cls.form, 'HTMLmode':cls.HTMLmode, 'film':cls.film, 'records':None if not cls.film else cls.film.get_comments(), 'curr_comment_id':None})
        else:
            return cls.redirect()

    @classmethod
    def redirect(cls):
        return HttpResponseRedirect(reverse('my-films'))


class FilmCreate(FilmView, CreateViewWithStamp):
    '''class to handle film create requests'''

    Form = FilmForm
    HTMLmode = 'film-create'

    @classmethod
    def after_post(cls):
        super().after_post()
        if cls.form.cleaned_data['image_from_url']:
            cls.save_image_from_url()
        elif cls.req.FILES and cls.req.FILES['image_from_file']:
            cls.save_image_from_file()
        elif cls.form.cleaned_data['remove_image']:
            cls.remove_image()


class FilmUpdate(FilmView, UpdateViewWithStamp):
    '''class to handle film update requests'''

    Form = FilmForm
    HTMLmode = 'film-update'

    @classmethod
    def after_post(cls):
        super().after_post()
        if cls.form.cleaned_data['image_from_url']:
            cls.save_image_from_url()
        elif cls.req.FILES and cls.req.FILES['image_from_file']:
            cls.save_image_from_file()
        elif cls.form.cleaned_data['remove_image']:
            cls.remove_image()
    

class FilmDelete(FilmView, DeleteView):
    '''class to handle film delete requests'''

    Form = FilmFormDelete
    HTMLmode = 'film-delete'

    @classmethod
    def before_post(cls):
        super().before_post()
        cls.remove_image()


class AllFilms(BaseListWithPaginator):
    '''class to handle list of all-films requests'''

    Model = Film

    @classmethod
    def query(cls):
        cls.records = cls.Model.objects.all().order_by('-updated_at')

    @classmethod
    def render(cls):
        cls.req.user.is_the_admin = True if cls.req.user.username==os.environ.get('ADMIN_USERNAME', None) else False
        return render(cls.req, 'films/film_list.html', {'subtitle':'All Films', 'records':cls.records, 'user':cls.req.user})


class MyFilms(BaseListWithPaginator):
    '''class to handle list of my-films requests'''

    Model = Film

    @classmethod
    def query(cls):
        cls.records = cls.Model.objects.filter(user=cls.req.user).order_by('-updated_at')

    @classmethod
    def render(cls):
        return render(cls.req, 'films/film_list.html', {'subtitle':'My Films', 'records':cls.records, 'user':cls.req.user})

    @classmethod
    def redirect(cls):
        return HttpResponseRedirect(reverse('my-films'))

##############################################################################

class CommentView(BaseView):
    '''class to handle comment requests'''

    Model = Comment
    Form = None
    film = None
    HTMLmode = None

    @classmethod
    def render(cls):
        cls.req.user.is_the_admin = True if cls.req.user.username==os.environ.get('ADMIN_USERNAME', None) else False
        return render(cls.req, 'films/film_comments.html', {'form':cls.form, 'HTMLmode': cls.HTMLmode, 'film':cls.film, 'records':cls.film.get_comments(), 'curr_comment_id': cls.id})

    @classmethod
    def redirect(cls):
        return HttpResponseRedirect(reverse('film-comments', args=[str(cls.film.id)]))


class FilmComments(CommentView, CreateViewWithStamp):
    '''class to display the comments of a film comments and also handle comment-create requests'''

    Form = CommentForm
    HTMLmode = 'comment-create'

    @classmethod
    def not_post(cls):
        super().not_post()
        cls.film = get_object_or_404(Film, pk=cls.id)
        cls.form.fields['film_id'].initial=cls.film.id

    @classmethod
    def after_post(cls):
        super().after_post()
        cls.film.updated_at = timezone.now()
        cls.film.save()


class CommentUpdate(CommentView, UpdateViewWithStamp):
    '''class to handle comment-update requests'''

    Form = CommentForm
    HTMLmode = 'comment-update'

    @classmethod
    def not_post(cls):
        super().not_post()
        cls.film = get_object_or_404(Film, pk=cls.model.film_id)
        cls.form.fields['film_id'].initial=cls.model.film_id

    @classmethod
    def after_post(cls):
        super().after_post()
        cls.film.updated_at = timezone.now()
        cls.film.save()


class CommentDelete(CommentView, DeleteView):
    '''class to handle comment-delete requests'''

    Form = CommentFormDelete
    HTMLmode = 'comment-delete'

    @classmethod
    def not_post(cls):
        super().not_post()
        cls.film = get_object_or_404(Film, pk=cls.model.film_id)
        cls.form.fields['film_id'].initial=cls.model.film_id


class AllComments(BaseListWithPaginator):
    '''class to handle list of all-comments requests'''

    Model = Comment

    @classmethod
    def query(cls):
        cls.records = cls.Model.objects.all().order_by('-updated_at')

    @classmethod
    def render(cls):
        cls.req.user.is_the_admin = True if cls.req.user.username==os.environ.get('ADMIN_USERNAME', None) else False
        return render(cls.req, 'films/comment_list.html', {'subtitle':'All Comments', 'records':cls.records, 'user':cls.req.user})


class MyComments(BaseListWithPaginator):
    '''class to handle list of my-comments requests'''

    Model = Comment

    @classmethod
    def query(cls):
        cls.records = cls.Model.objects.filter(user=cls.req.user).order_by('-updated_at')

    @classmethod
    def render(cls):
        return render(cls.req, 'films/comment_list.html', {'subtitle':'My Comments', 'records':cls.records, 'user':cls.req.user})