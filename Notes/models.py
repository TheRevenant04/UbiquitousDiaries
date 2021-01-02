from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField

#Sets the unique constraint on the 'email' field to True.
User._meta.get_field('email')._unique = True

class Diary(models.Model):
    """
    A class that extends Django's Model class.
    It is used to model a user's Diary objects.

    Attributes
    ----------
    author : str
        The user's username used to distinguish each diary in the database.
        It is a foreign key to the User relation in the database.
    title : str
        The diary name.
    create_date : datetime.datetime
        The diary creation date and time.

    Methods
    -------
    __str__
        Returns a string representation of the Diary object.
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    create_date = models.DateTimeField(default = timezone.now)

    class Meta:
        """
        An inner class that specifies the meta data of the Model class.
        In this case the model's default field configurations have been Overrided.

        Attributes
        ----------
        constraints : list
            Contains constraints to be applied on the model.
            In this case a composite unique key is defined on 'author' and 'title' fields.
        """
        constraints = [
            models.UniqueConstraint(fields = ["author", "title"], name='unique_diaries')
        ]

    def __str__(self):
        """
        A method that represents a string representation of a Diary object.
        In this case, the 'title' of the diary is used as the string representation.

        Returns
        -------
        self.title : str
            The title of the diary.
        """
        return self.title


class Note(models.Model):
    """
    A class that extends Django's Model class.
    It is used to model a user's Note objects of a particular Diary.

    Attributes
    ----------
    diary : object
        The user's username used to distinguish each diary in the database.
        It is a foreign key to the Diary relation in the database.
    title : str
        The note's name.
    content : str
        The note's content.
    create_date : datetime.datetime
        The note creation date and time.
    last_update_time : datetime.datetime
        The note's last update time.

    Methods
    -------
    __str__
        Returns a string representation of the Note object.
    """
    diary = models.ForeignKey(Diary, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    create_date = models.DateTimeField(default = timezone.now)
    last_update_time = models.DateTimeField(default = timezone.now)

    class Meta:
        """
        An inner class that specifies the meta data of the Model class.
        In this case the model's default field configurations have been Overrided.

        Attributes
        ----------
        constraints : list
            Contains constraints to be applied on the model.
            In this case a composite unique key is defined on 'diary' and 'title' fields.
        """
        constraints = [
            models.UniqueConstraint(fields=["diary", "title"], name='unique_notes')
        ]

    def __str__(self):
        """
        A method that returns a string representation of a Note object.
        In this case, the 'title' of the note is used as the string representation.

        Returns
        -------
        self.title : str
            The title of the note.
        """
        return self.title
