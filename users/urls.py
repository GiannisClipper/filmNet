# urls.py

from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView 
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

    path('login/', LoginView.as_view(template_name='registration/login_form.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password_change/', PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password-change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),

    path('password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password-reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_change_reset_complete.html'), name='password_reset_complete'),

    path('user/<int:id>/delete/', views.user_delete, name='user-delete'),

    path('list/', views.list, name='users-list'),
]
