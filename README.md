# < hang >
🔡 A hangman game built with Angular and Flask

![alt text](https://github.com/igorp1/hang/blob/master/hang-demo.gif?raw=true "<hang demo>")


## Dev system requirements:
You must have the following intalled in your machine:

- [node](https://nodejs.org/en/)
- [npm](https://www.npmjs.com/get-npm)
- [python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

This project was built using:

| Program       | Version       |
| ------------- |:-------------:|
| node          | 8.9.4         |
| npm           | 5.6.0         |
| python        | 2.7.14        |
| pip           | 9.0.1         |
| virtualenv    | 15.1.0        |


## Get started

### /hang-backend

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


### /hang-webapp
To install dependencies:
```
npm i
```
To start the aplication on your local run:
```
ng serve
```