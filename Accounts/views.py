from Accounts.forms import SignUpForm, SignInForm, ForgotUserNameForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView

class SendUsernameDoneView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render a response to the user on emailing them their username.

    Attributes
    ----------
    template_name : str
        The html page for the user response.
    """
    template_name = "Accounts/username_send_done.html"


class SignUpCompleteView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render a response to the user on confirming their email after signing up.

    Attributes
    ----------
    template_name : str
        The html page for the user response.
    """
    template_name = "Accounts/signup_complete.html"


class SignUpDoneView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render a response to the user on signing up.

    Attributes
    ----------
    template_name : str
        The html page for the user response.
    """
    template_name = "Accounts/signup_done.html"


def signup(request):
    """
    A view that:
        renders the signup page.
        Validates the SignUpForm data.
        Creates a new User object with 'is_active' status as 'False' if the SignUpForm POST data is valid.
        Sends an email confirmation email to a newly created user.
        An activation link is created by using:
            The desired protocol.
            the current domain name.
            a base64 encoded unique user id.
            Django's default token generator.
        A user cannot sign in until the email is not confirmed.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.

    Returns
    -------
    HttpResponseRedirect
        A request to the signup_done page when the user submits valid POST data and a new User object is created.
    HttpResponse
        A new SignUpForm instance when the user accesses the signup page.
        A SignUpForm instance with errors when the user enters invalid data.

    Raises
    ------
    ValidationError
        If the form data is not correct or as per guidelines.
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        i_agree = request.POST.get("i_agree", False)
        if form.is_valid() and i_agree:
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Confirm your email.'
            message = render_to_string('Accounts/new_account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                'protocol': 'http',
            })
            email_id = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[email_id])
            email.send()
            return redirect('Accounts:signup_done')
        return render(request, 'Accounts/signup.html', {'form':form, 'i_agree':i_agree})
    else:
        form = SignUpForm()
        return render(request, 'Accounts/signup.html', {'form':form})


@login_required
def myaccount(request):
    """
    A view that renders the personal details of an authenticated user.
    This view can be accesssed on if a user is authenticated or is signed in.
    It cannot be accessed by anonymous users.
    the login_required decorator ensures that this view can be only accessed by signed in users.
    Anonymous users are redirected to the signin page.
    The view populates a UpdateUserForm once rendered.
    The user is free to change name credentials and username which are updated in the database.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.

    Returns
    -------
    HttpResponseRedirect
        A request to the same view when the user submits valid POST data and a the User object is updated.
    HttpResponse
        A user accesses the personal details page to view their information.

    Raises
    ------
    ValidationError
        If the form data is not correct or as per guidelines.
    """
    if request.method == "POST":
        form=UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('Accounts:myaccount')
    form = UpdateUserForm(instance=request.user)
    return render(request, 'Accounts/myaccount.html',{'form': form})


def email_confirmation(request, uidb64, token):
    """
    This view validates an email confirmation link when accessed by a user.
    The base64 encoded unique id is decoded and the token validity is checked.
    If both items are valid, then the user's 'is_active' status is set to 'True'.
    If one or both the data items is invalid, an error message is rendered.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.
    uidb64 : str
        The base64 encoded value of a user's unique id.
    token : str
        A token used for generating the one time email confirmation link.

    Returns
    -------
    HttpResponseRedirect
        A request to the SignUpCompleteView when the user accesses the email confirmation message.
    HttpResponse
        A response indicating an invalid link.

    Raises
    ------
    TypeError
    ValueError
    OverflowError
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('Accounts:signup_complete')
    else:
        message = "Confirmation link is invalid!"
        return render(request, 'Accounts/signup_complete.html', {'message':message})


def send_username(request):
    """
    A view that sends an email to a user if they forget their username_send.
    An email is sent to a registered email address that the user enters after validation.
    A response message is rendered irrespective of whether the email is sent or not. This
    is done in order to avoid exposure of user data.

    Parameters
    ----------
    request : HttpRequest
        An HttpRequest object that contains metadata about a request.

    Returns
    -------
    HttpResponseRedirect
        A request to the SendUsernameDoneView when the user submits valid POST data and a email is sent to the user with their username.
    HttpResponse
        A user accesses the forgot username page.

    Raises
    ------
    ValidationError
        If the form data is not correct or as per guidelines.
    """
    if request.method == "POST":
        form = ForgotUserNameForm(request.POST)
        if form.is_valid():
            mail_subject = 'Account username request.'
            email_id = form.cleaned_data.get("email")
            users = User.objects.filter(email=email_id)
            if users.exists():
                user = users[0]
                message = render_to_string('Accounts/username_send_email.html', {
                    'user': user
                })
                email = EmailMessage(mail_subject, message, to=[email_id])
                email.send()

            return redirect('Accounts:send_username_done')
        return render(request, 'Accounts/username_send_form.html', {'form':form})
    else:
        form = ForgotUserNameForm()
        return render(request, 'Accounts/username_send_form.html', {'form':form})
