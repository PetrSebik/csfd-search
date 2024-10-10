## CSFD search example project in django
* create a new database in Postgres on your system
* create a `.env` file and fill the details for Postgres DB connection on your system, 
you can use `env.example` file as a template
* run the database migration with command `python manage.py migrate`
* download the data from csfd.cz with command `python manage.py download` (it may take a minute)
* run the server with command `python manage.py runserver`