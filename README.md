1. django-admin startproject project_name- To create a Django Project
2. python manage.py runserver - To run the server
3. create requirement.txt to document all the library we are using.
4. .gitignore which help reduce the bandwidth/size of the app (eg avoid sending thing like nodemodule, .env file, build files etc.
5. Django REST framework is a powerful and flexible toolkit for building Web APIs with Django
   djangorestframework-simplejwt[blacklist]- used for for authenication.
6. Use Toptal to generate .gitignore files.
7. Register the new libraries and application created with the project parent folder appending them in the Installed_APPs with the setting.py
python manage.py startapp <app_name> - for generating a module within the larger project.
python manage.py makemigrations- prepares columns and raws, checks for new changes in the database.
python manage.py migrate- migrates database
python manage.py createsuperuser- creates superuser(Admin)