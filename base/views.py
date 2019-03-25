# views.py

from django.contrib.auth.decorators import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms

from django.utils import timezone

import os, glob
from urllib import request
from PIL import Image

##############################################################################

def admin_required(function):
    '''decorator to check if logged in user is admin'''

    @wraps(function)
    def decorator(req, *args, **kwargs):
        if req.user and req.user.username == os.environ.get('ADMIN_USERNAME', None):
            return function(req, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('login'))
    return decorator

##############################################################################

class FileHandler:
    '''class to handle file upload'''

    url_source = None
    file_source = None
    path = ''
    name = None
    ext = ''

    @classmethod
    def fullname(cls):
        return f'{cls.path}{cls.name}' + f'.{cls.ext}' if cls.ext else ''

    @classmethod
    def save_from_file(cls):
        with open(cls.fullname(), 'wb+') as destination:
            for chunk in cls.file_source.chunks():
                destination.write(chunk)

    @classmethod
    def save_from_url(cls):
        handler = request.urlopen(cls.url_source)
        data = handler.read()
        with open(cls.fullname(), 'wb') as file:
            file.write(data)
        #request.urlretrieve(cls.url, cls.fullname()) in python 2

    @classmethod
    def delete(cls, mask=None):
        if not mask: mask = cls.fullname()
        found = glob.glob(mask)
        for f in found:
            os.remove(f)


class FileImageHandler(FileHandler):
    '''class to handle file upload (extended for images)'''

    @classmethod
    def resize(cls, width=512, height=512):
        im = Image.open(cls.fullname())
        im.thumbnail((width, height))
        im.save(cls.fullname())

##############################################################################

class BaseView:
    '''class to handle record requests'''

    req = None
    Model = None
    model = None
    Form = None
    form = None
    id = None

    @classmethod
    def run(cls, req, id=None):
        cls.req = req
        cls.id = id
        cls.model = cls.Model()

        if cls.req.method == 'POST':
            print('\n\n\n', cls.req.POST, '\n\n\n')
            cls.form = cls.Form(cls.req.POST, cls.req.FILES)
            if 'submit_ok' in cls.req.POST: #on [save] / [ok] button clicks
                if cls.form.is_valid():
                    cls.before_post()
                    cls.post()
                    cls.after_post()
                    return cls.redirect()
            else: #on cancel button click
                return cls.redirect()
        else:
            cls.not_post()
        return cls.render()

    @classmethod
    def before_post(cls):
        pass

    @classmethod
    def post(cls):
        pass

    @classmethod
    def after_post(cls):
        pass

    @classmethod
    def not_post(cls):
        pass

    @classmethod
    def from_form_to_model(cls):
        for k, v in cls.form.cleaned_data.items(): #iterate all form fields and set values in model
            if hasattr(cls.model, k): #k!='csrfmiddlewaretoken':
                setattr(cls.model, k, v)

    @classmethod
    def from_model_to_form(cls):
        for k in cls.form.fields.keys(): #iterate all form fields and get values from model
            if hasattr(cls.model, k): #k!='csrfmiddlewaretoken':
                cls.form.fields[k].initial=getattr(cls.model, k)

    @classmethod
    def render(cls):
        return HttpResponse('No rendering setup.')

    @classmethod
    def redirect(cls):
        return HttpResponseRedirect('/')


class CreateView(BaseView):
    '''class to handle record create requests'''

    @classmethod
    def before_post(cls):
        cls.from_form_to_model()

    @classmethod
    def post(cls):
        cls.model.save()

    @classmethod
    def not_post(cls):
        cls.form = cls.Form()


class UpdateView(BaseView):
    '''class to handle record update requests'''

    @classmethod
    def before_post(cls):
        cls.model = get_object_or_404(cls.Model, pk=cls.form.cleaned_data['id'])
        cls.from_form_to_model()

    @classmethod
    def post(cls):
        cls.model.save()

    @classmethod
    def not_post(cls):
        cls.model = get_object_or_404(cls.Model, pk=cls.id)
        cls.form = cls.Form()
        cls.from_model_to_form()


class DeleteView(BaseView):
    '''class to handle record delete requests'''

    @classmethod
    def before_post(cls):
        cls.model = get_object_or_404(cls.Model, pk=cls.form.cleaned_data['id'])

    @classmethod
    def post(cls):
        cls.model.delete()

    @classmethod
    def not_post(cls):
        cls.model = get_object_or_404(cls.Model, pk=cls.id)
        cls.form = cls.Form()
        cls.from_model_to_form()

##############################################################################

class CreateViewWithStamp(CreateView):
    '''class to handle record create requests (extended with stamp)'''

    @classmethod
    def before_post(cls):
        super().before_post()
        cls.model.user = cls.req.user
        cls.model.created_at = timezone.now()
        cls.model.updated_at = cls.model.created_at

class UpdateViewWithStamp(UpdateView):
    '''class to handle record update requests (extended with stamp)'''

    @classmethod
    def before_post(cls):
        super().before_post()
        cls.model.updated_at = timezone.now()

##############################################################################

class BaseList:
    '''class to handle list requests'''
    req = None
    Model = None
    records = None

    @classmethod
    def run(cls, req):
        cls.req = req
        cls.query()
        return cls.render()

    @classmethod
    def query(cls):
        cls.records = cls.Model.objects.all()

    @classmethod
    def render(cls):
        return HttpResponse('No rendering setup.')


class BaseListWithPaginator(BaseList):
    '''class to handle list requests (extended with paginator)'''

    paginator = None

    @classmethod
    def run(cls, req):
        cls.req = req
        page = cls.req.GET.get('page', 1)
        cls.query()
        cls.paginator = Paginator(cls.records, 5)
        try:
            cls.records = cls.paginator.page(page)
        except PageNotAnInteger:
            cls.records = cls.paginator.page(1)
        except EmptyPage:
            cls.records = cls.paginator.page(cls.paginator.num_pages)
        return cls.render()