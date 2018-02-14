# < hang >
🔡 A hangman game built with Angular and Flask

## Get started

### Back End
To setup the virtual env:
```
virtualenv hang_env
source hang_env/bin/activate 
pip install -r requirements.txt
```
To activate the virtualenv:
```
source hang_env/bin/activate 
```
To run the aplication:
```
APP_ENV=dev
python manage.py runserver
```
To run unit tests:
```
nosetests
```
If you add new python packages make sure to:
```
pip freeze > requirements.txt
```
To implement model changes to the DB:
```
python manage.py db migrate
python manage.py db upgrade
``` 


### Front End
To start the aplication on your local run:
```
ng serve
```