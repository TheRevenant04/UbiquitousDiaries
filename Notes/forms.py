from django import forms
from .models import Diary, Note

class DiaryForm(forms.ModelForm):
    """
    This class extends Django's ModelForm.
    This class is used for creating a form for creating user diaries.
    """
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
        model = Diary
        fields = ["title"]

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
        super(DiaryForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['title'].widget.attrs.update({'class':'form-control', 'placeholder':"Enter your diary's title here"})


class EditNoteForm(forms.ModelForm):
    """
    This class extends Django's ModelForm.
    This class is used for creating a form for editing a user's notes.
    """

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
        model = Note
        fields = ["title", "content"]

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
        super(EditNoteForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['title'].widget.attrs.update({'class':'form-control', 'placeholder':"Enter your note's title here"})
        self.fields['content'].widget.attrs.update({'class':'form-control', 'placeholder':'Enter your content here'})


class NewNoteForm(forms.ModelForm):
    """
    This class extends Django's ModelForm.
    This class is used for creating a form for creating user notes in a diary.
    """

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
        model = Note
        fields = ["title"]

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
        super(NewNoteForm, self).__init__(*args, **kwargs)

        #Changes the default form widgets appearance of every field in the form class using update()
        self.fields['title'].widget.attrs.update({'class':'form-control', 'placeholder':"Enter your note's title here"})
