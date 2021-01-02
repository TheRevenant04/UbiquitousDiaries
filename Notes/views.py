from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import TemplateView
from Notes.forms import DiaryForm, EditNoteForm, NewNoteForm
from Notes.models import Diary, Note

class HomePageView(TemplateView):
    """
    A view that extends Django's default TemplateView.
    This view is used to render the home page to a user.

    Attributes
    ----------
    template_name : str
        The html page for the user response.
    """
    template_name = "Notes/index.html"


@login_required
def delete_diary(request, diary):
    """
    A view that deletes a user's diary.
    The diary is extracted by matching the user's diary to the diary field of the Note object.
    This view can only be accessed if a user is authenticated.
    The login_required decorator is used to ensure the previous point.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.
    diary : str
        The user's diary name.

    Returns
    -------
    HttpResponseRedirect
        redirect to the my_diaries view.
    """
    my_diary = Diary.objects.get(title=diary)
    my_diary.delete()
    return redirect('Notes:my_diaries')


@login_required
def delete_note(request, diary, note):
    """
    A view that deletes a user's diary note.
    The note is extracted by matching the user's diary to the diary field of the Note object
    and the user's note to the Note title field.
    This view can only be accessed if a user is authenticated.
    The login_required decorator is used to ensure the previous point.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.
    diary : str
        The user's diary name.
    note : str
        The user's note.
    Returns
    -------
    HttpResponseRedirect
        redirect to the diary_content view.
    """
    my_diary = Diary.objects.get(title=diary)
    cond1 = Q(title=note)
    cond2 = Q(diary = my_diary)
    Note.objects.get(cond1 & cond2).delete()
    return redirect('Notes:diary_content', diary=diary)


@login_required
def diary_content(request, diary):
    """
    A view that renders a user's diary content and a NewNoteForm for adding new notes.
    The notes are extracted by matching the user's diary to the diary field of the Note object.
    Duplicate note names are not allowed in the same diary of a user.
    This view can only be accessed if a user is authenticated.
    The login_required decorator is used to ensure the previous point.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.
    diary : str
        The user's diary name.

    Returns
    -------
    HttpResponseRedirect
        A request to the note_content view when the user submits valid POST data and a new Note object is created.
    HttpResponse
        A new NewNoteForm instance when the user accesses the diary_content page.
        A NewNoteForm instance with errors when the user enters invalid data or enters an existing note name.

    Raises
    ------
    ValidationError
        If the form data is not correct or as per guidelines.
    """
    my_diary = Diary.objects.get(title=diary)
    notes = Note.objects.filter(diary=my_diary.id).order_by('title')
    if request.method == "POST":
        form = NewNoteForm(request.POST)
        title = request.POST["title"]
        note = Note.objects.filter(title=title, diary=my_diary)
        if note:
            error_message = "This note already exists"
            form = DiaryForm()
            return render(request, 'Notes/diary_content.html', {'diary':diary, 'error_message':error_message, 'form':form, 'notes':notes})
        if form.is_valid():
            note = form.save(commit=False)
            note.diary = my_diary
            note.create_date = timezone.now()
            note.last_update_time = timezone.now()
            note.save()
            return redirect('Notes:note_content', diary=diary, note=note)
        return render(request, 'Notes/diary_content.html', {'diary':diary, 'form':form, 'notes':notes})
    else:
        form = NewNoteForm()
        return render(request, 'Notes/diary_content.html', {'diary':diary, 'form':form, 'notes':notes})


@login_required
def my_diaries(request):
    """
    A view that renders a user's diaries and a DiaryForm for adding new diaries.
    The diaries are extracted by matching the user's current username to the author field of the Diary object.
    Duplicate diary names are not allowed for a user.
    This view can only be accessed if a user is authenticated.
    The login_required decorator is used to ensure the previous point.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.

    Returns
    -------
    HttpResponseRedirect
        A request to the diary_content view when the user submits valid POST data and a new Diary object is created.
    HttpResponse
        A new DiaryForm instance when the user accesses the mydiaries page.
        A DiaryForm instance with errors when the user enters invalid data or enters an existing diary name.

    Raises
    ------
    ValidationError
        If the form data is not correct or as per guidelines.
    """
    if request.method == "POST":
        form = DiaryForm(request.POST)
        diary_title = request.POST["title"]
        author = request.user
        cond1 = Q(title=diary_title)
        cond2 = Q(author = author)
        diaries = Diary.objects.filter(cond1 & cond2)
        if diaries:
            error_message = "This diary already exists"
            form = DiaryForm()
            diaries = Diary.objects.filter(author=request.user).order_by('title')
            return render(request, 'Notes/my_diaries.html', {'form':form, 'diaries':diaries, 'error_message':error_message})
        if form.is_valid():
            diary = form.save(commit=False)
            diary.author = author
            diary.create_date = timezone.now()
            diary.save()
            return redirect('Notes:diary_content',diary=diary)
        diaries = Diary.objects.filter(author=request.user).order_by('title')
        return render(request, 'Notes/my_diaries.html', {'form':form, 'diaries':diaries})
    else:
        form = DiaryForm()
        diaries = Diary.objects.filter(author=request.user).order_by('title')
        return render(request, 'Notes/my_diaries.html', {'form':form, 'diaries':diaries})


@login_required
def note_content(request, diary ,note):
    """
    A view that renders a user's note content and a EditNoteForm for editing notes.
    The notes are extracted by matching the user's diary to the diary field of the Note object
    and the user's note to the title field of Note.
    This view can only be accessed if a user is authenticated.
    The login_required decorator is used to ensure the previous point.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.
    diary : str
        The user's diary name.
    note : str
        The user's note name in the diary.

    Returns
    -------
    HttpResponseRedirect
        A request to the note_content view when the user submits valid POST data and a existing Note instance is rendered.
    HttpResponse
        A new EditNoteForm instance when the user accesses the note_content page.

    Raises
    ------
    ValidationError
        If the form data is not correct or as per guidelines.
    """
    my_diary = Diary.objects.get(title=diary)
    cond1 = Q(title=note)
    cond2 = Q(diary = my_diary)
    note = Note.objects.get(cond1 & cond2)
    if request.method == "POST":
        form = EditNoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.last_update_time=timezone.now()
            note.save()
            return redirect('Notes:note_content', diary=diary, note=note)
    form = EditNoteForm(instance=note)
    return render(request, 'Notes/notes_content.html', {'diary':diary, 'form':form, 'note':note})


@login_required
def note_read_mode(request, diary, note):
    """
    A view that renders a user's note content in read mode.
    The notes are extracted by matching the user's diary to the diary field of the Note object
    and the user's note to the title field of Note.
    This view can only be accessed if a user is authenticated.
    The login_required decorator is used to ensure the previous point.

    Parameters
    ----------
    request : HttpRequest object
        An HttpRequest object that contains metadata about a request.
    diary : str
        The user's diary name.
    note : str
        The user's note name in the diary.

    Returns
    -------
    HttpResponse
        A new EditNoteForm instance when the user accesses the note_content page.
    """
    my_diary = Diary.objects.get(title=diary)
    cond1 = Q(title=note)
    cond2 = Q(diary = my_diary)
    note = Note.objects.get(cond1 & cond2)
    return render(request, 'Notes/notes_content.html', {'diary':diary, 'note':note})
