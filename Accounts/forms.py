from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User

class ChangePasswordForm(PasswordChangeForm):
    """
    This class extends Django's inbuilt PasswordChangeForm.
    This class is used for creating a form for changing passwords.
    """
    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['old_password'].widget.attrs.update({'class':'form-control', 'placeholder':'Old Password'})
        self.fields['new_password1'].widget.attrs.update({'class':'form-control', 'placeholder':'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control', 'placeholder':'Confirm New Password'})


class ForgotPasswordForm(PasswordResetForm):
    """
    A class that inherits Django's inbuilt PasswordResetForm.
    It is used to create a user form for resetting passwords.
    """
    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['email'].widget.attrs.update({'class':'form-control', 'placeholder':'Email'})


class ForgotUserNameForm(forms.Form):
    """
    A class that extends Django's default Form class.
    This class is used for creating forms used for emailing users their username in case they forget.

    Attributes
    ----------
    email : str
        The user's email.
    """
    email = forms.EmailField(max_length=100)

    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(ForgotUserNameForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['email'].widget.attrs.update({'class':'form-control', 'placeholder':'Email'})


class NewPasswordForm(SetPasswordForm):
    """
    A class that extends Django's inbuilt SetPasswordForm.
    This class is used to create a form for creating new user passwords in case a user forgets their account password.
    """
    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(NewPasswordForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['new_password1'].widget.attrs.update({'class':'form-control', 'placeholder':'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control', 'placeholder':'Confirm New Password'})


class SignInForm(AuthenticationForm):
    """
    A form class that inherits Django's inbuilt AuthenticationForm.
    It is used for creating a form for user sign in.
    It allows users that have an 'active' account status to sign in.
    """
    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(SignInForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update().
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Username'})
        self.fields['password'].widget.attrs.update({'class':'form-control', 'placeholder':'Password'})


class SignUpForm(UserCreationForm):
    """
    A form class that inherits Django's inbuilt UserCreationForm.
    It is used for signing up new users for the web site.
    It uses the default User model to create user instances.
    However, the attributes specified below have been added to the default User model.

    Attributes
    ----------
    first_name : str
        The user's first name.
    last_name : str
        The user's surname
    email : str
        The user's email address.

    Methods
    -------
    save(commit=True)
        Overrides Django's default ModelForm class save() method.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=100)

    class Meta:
        """
        An inner class that specifies the meta data of the ModelForm class.
        In this case the form's default field configurations have been Overrided.

        Attributes
        ----------
        model : obj
            Specifies the model class to be used for creating a form.
        fields : list
            Specifies the fields to be used in the form.
        """
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(SignUpForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['first_name'].widget.attrs.update({'class':'form-control', 'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control', 'placeholder':'Last Name'})
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Username'})
        self.fields['email'].widget.attrs.update({'class':'form-control', 'placeholder':'Email'})
        self.fields['password1'].widget.attrs.update({'class':'form-control', 'placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class':'form-control', 'placeholder':'Confirm Password'})

    def save(self, commit=True):
        """
        Overrides the default ModelForm save().
        Adds class attributes to the model for saving changes.

        Parameters
        ----------
        commit : bool, optional
            Sets the flag to True or False for commiting changes to the database.
            The default value is True.

        Returns
        -------
        user : object
            The user object.
        """
        user = super(SignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    """
    A class that extends Django's ModelForm.
    This class is used to update a user's personal data.

    Attributes
    ----------
    first_name : str
        The user's first name.
    last_name : str
        The user's last name.

    Methods
    -------
    save(commit=True)
        Overrides Django's default ModelForm class save() method.
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        """
        An inner class that specifies the meta data of the ModelForm class.
        In this case the form's default field configurations have been Overrided.

        Attributes
        ----------
        model : obj
            Specifies the model class to be used for creating a form.
        fields : list
            Specifies the fields to be used in the form.
        """
        model = User
        fields = ("first_name", "last_name", "username")

    def __init__(self, *args, **kwargs):
        """
        Overrides the default form widgets for modifying the form field appearance.

        Parameters
        ----------
        *args
            Non key-worded variable number arguments.
        **kwargs : dict
            Variable dictionary arguments.
        """
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['first_name'].widget.attrs.update({'class':'form-control', 'placeholder':'First Name'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control', 'placeholder':'Last Name'})
        self.fields['username'].widget.attrs.update({'class':'form-control', 'placeholder':'Username'})

    def save(self, commit=True):
        """
        Overrides the default ModelForm save().
        Adds class attributes to the model for saving changes.

        Parameters
        ----------
        commit : bool, optional
            Sets the flag to True or False for commiting changes to the database.
            The default value is True.

        Returns
        -------
        user : object
            The user object.
        """
        user = super(UpdateUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
