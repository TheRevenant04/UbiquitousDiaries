# UbiquitousDiaries
A simple note taking web app created using python's Django framework.

## Description
* **UbiquitousDiaries** is a simple note taking application that can be used by anyone.
* A user has to create **diaries** to store their notes. This ensures that the notes are segregated as per the user's needs. 
* A user can store various **notes** in any diary and freely edit them.
* The web app uses a robust editor, **django-ckeditor**. More about the editor https://pypi.org/project/django-ckeditor/.
* The web app provides security to a user's data by providing authentication and authorization.
* The web app also stores a user's password in hashed form.

## Screenshots
![SignUp page](/static/images/signup.png)
![SignNn page](/static/images/signin.png)
![Diaries page](/static/images/diaries.png)
![EditNote page](/static/images/editnote.png)

## Requirements
* Python 3.9.0
* Django 3.1.4
* django-ckeditor 6.0.0

## How to Use?
#### Project Configuration
The project is configured to use the **gmail mailserver** for sending emails to users. If you wish to use this configuration, fill your gmail email address in the **EMAIL_HOST_USER** and password in the **EMAIL_HOST_PASSWORD** in the **DiaryApp/settings.py** file(This configuration also works on localhost provided you are connected to the internet). The code looks like this in the settings.py file:
>EMAIL_USE_TLS = True<br>
EMAIL_HOST = "smtp.gmail.com"<br>
EMAIL_HOST_USER = "Your Email"<br>
EMAIL_HOST_PASSWORD = "Your password"<br>
EMAIL_PORT = 587

However, if you are running the project on your local machine and dont wish to use the gmail mailserver then you can comment the following lines in the 'settings.py' file 
>EMAIL_USE_TLS = True<br>
EMAIL_HOST = "smtp.gmail.com"<br>
EMAIL_HOST_USER = "Your Email"<br>
EMAIL_HOST_PASSWORD = "Your password"<br>
EMAIL_PORT = 587

and add the following line in the 'settings.py' file.

>EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   
 #### Project Setup  
1. (**Skip this step if you already have the required version**)Install Python.

1. Clone the project from the project repo
   >$git clone https://github.com/TheRevenant04/UbiquitousDiaries.

1. (**Optional but recommended**) Create a virtual environment in the project folder. Replace **name** with a name you of your choice.
   >(path to your project)$python -m venv **name**  

1. (**Skip this step if you skipped the previous step**)Activate the virtual environment. Replace **name** with **name** from the previous step.
   >(path to your project)$**name**\scripts\activate
   
1. Install the required packages.
   >(path to your project)$pip install -r requirements.txt

1. Create the project database.
   >(path to your project)$python manage.py migrate
   
1. Run the project.
   >(path to your project)$python manage.py runserver
   
1.Open a browser and enter the following URL
  >127.0.0.1:8000
