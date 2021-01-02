from . import views
from django.urls import path

#The app's namespace.
app_name = "Notes"

urlpatterns = [
#The url to the home page.
path('', views.HomePageView.as_view(), name = 'home_page'),
#A url mapped to a view that renders a user's diaries and new diary form.
path('mydiaries/', views.my_diaries, name = 'my_diaries'),
#A url mapped to a view that renders a user's diary content and a note form.
path('mydiaries/<diary>/', views.diary_content, name ='diary_content'),
#A url mapped to a view that deletes a user's diary on their request.
path('mydiaries/<diary>/delete/', views.delete_diary, name ='delete_diary'),
#A url mapped to a view that renders a user's note in read mode.
path('mydiaries/<diary>/<note>/delete/', views.delete_note, name='delete_note'),
#A url mapped to a view that renders a user's diaries and new diary form.
path('mydiaries/<diary>/<note>/edit/', views.note_content, name='note_content'),
#A url mapped to a view that renders a user's note content.
path('mydiaries/<diary>/<note>/read/', views.note_read_mode, name='note_read_mode'),
]
