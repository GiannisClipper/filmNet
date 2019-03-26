# views.py

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
import os

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import User #from django.contrib.auth.models import User
from .tokens import account_activation_token
from .forms import SignupForm, UserFormDelete
from base.views import DeleteView, BaseListWithPaginator

from django.contrib.auth.decorators import login_required
from base.views import admin_required

##############################################################################

def signup(req):
    '''function to handle signup requests'''

    if req.method == 'POST':
        form = SignupForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(req)
            mail_subject = '[filmNet] Account activation instructions'
            message = render_to_string('registration/signup_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please check your email address to complete the registration')
    else:
        form = SignupForm()
    return render(req, 'registration/signup_form.html', {'form': form})


def activate(req, uidb64, token):
    '''function to handle confirm-registration requests'''

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(req, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.') #return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')

##############################################################################

@login_required 
@admin_required
def user_delete(req, id): return UserDelete.run(req, id)

class UserDelete(DeleteView):
    '''class to handle user delete requests'''

    Model = User
    Form = UserFormDelete

    @classmethod
    def render(cls):
        return render(cls.req, 'users/user_form_delete.html', {'form':cls.form, 'is_admin':True, 'user_to_delete':cls.model})

    @classmethod
    def redirect(cls):
        return HttpResponseRedirect(reverse('users-list'))


@login_required
def list(req): return UserList.run(req)

class UserList(BaseListWithPaginator):
    '''class to handle list of users requests'''

    Model = User
    is_admin = None

    @classmethod
    def query(cls):
        cls.is_admin = cls.req.user and cls.req.user.username == os.environ.get('ADMIN_USERNAME', None)
        cls.records = cls.Model.objects.all() if cls.is_admin else cls.Model.objects.filter(is_active=True)

    @classmethod
    def render(cls):
        return render(cls.req, 'users/user_list.html', {'is_admin':cls.is_admin ,'records':cls.records})