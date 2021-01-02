"""Ubiquitous Diaries URL Configuration

The `urlpatterns` list routes URLs to views.
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from Accounts.forms import SignInForm, ForgotPasswordForm, NewPasswordForm, ChangePasswordForm
from django.urls import reverse_lazy

#Namespace for the Accounts app.
app_name = 'Accounts'

urlpatterns = [
    #A url mapped to a view that generates an email confirmation request.
    path('email_confirmation/<uidb64>/<token>/',views.email_confirmation, name='email_confirmation'),
    #A url mapped to a view that renders the user's my account page.
    path('myaccount/', views.myaccount, name = 'myaccount'),
    #A url mapped to a view that renders a password change page for signed in users.
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='Accounts/password_change_form.html', form_class=ChangePasswordForm, success_url=reverse_lazy('Accounts:password_change_done')), name='password_change'),
    #A url mapped to a view that generates a response when a signed in user changes their password.
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='Accounts/password_change_done.html'), name='password_change_done'),
    #A url mapped to a view that renders the reset password page.
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Accounts/password_reset.html', success_url=reverse_lazy('Accounts:password_reset_done'),form_class=ForgotPasswordForm, email_template_name='Accounts/password_reset_email.html', subject_template_name='Accounts/password_reset_subject.txt'), name='password_reset'),
    #A url mapped to a view that renders a response on a user's request to reset their password on the reset password page.
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Accounts/password_reset_done.html'), name='password_reset_done'),
    #A url mapped to a view that generates a reset password link that is emailed to the user's email address.
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Accounts/password_reset_confirm.html", form_class=NewPasswordForm, success_url=reverse_lazy('Accounts:password_reset_complete')), name='password_reset_confirm'),
    #A url mapped to a view that renders a message when the user opens the reset password link.
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset_complete.html'), name='password_reset_complete'),
    #A url mapped to a view that renders the signin page.
    path('signin/', auth_views.LoginView.as_view(template_name='Accounts/signin.html', authentication_form=SignInForm, redirect_field_name="Notes/my_diaries.html"), name = 'login'),
    #A url mapped to a view that handles a user signout.
    path('signout/', auth_views.LogoutView.as_view(), name = 'logout'),
    #A url mapped to a view that renders the signup page.
    path('signup/', views.signup, name = 'signup'),
    #A url mapped to a view that renders a response when a user confirms their email address.
    path('signup/complete/',views.SignUpCompleteView.as_view(), name='signup_complete'),
    #A url mapped to a view that renders a response when a user signs up.
    path('signup/done/',views.SignUpDoneView.as_view(), name='signup_done'),
    #A url mapped to a view that renders a forgot username page.
    path('username_send/', views.send_username, name='send_username'),
    #A url mapped to a view that renders a response when a user's username is emailed to their email address.
    path('username_send_done/',views.SendUsernameDoneView.as_view(), name='send_username_done'),
]
