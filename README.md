# python-django-stock
Stock information provider. There are fifty stocks, components of 0050.TW, contained in `demodata` folder.

## Project Overview
### Screenshots

- Homepage

![](/screenshots/hompage.png")

- Register

![](/screenshots/register.png")

- Login & Third-Party Connect (Facebook and Google)

![](/screenshots/login.png")

- Forgot Password

![](/screenshots/forgotpwd.png")

- Search

![](/screenshots/search.png")

- Basic Stock Information

![](/screenshots/basic_info.png")

- Chips Stock Information

![](/screenshots/chips_info.png")

- Stock Picking

![](/screenshots/pick.png")

- Stock Picking Result

![](/screenshots/pick_result.png")


### Functinos:

+ Sign in through thrid-party accounts(Facebook and Google).
+ Easy collect users' email accounts
+ Viewing stock's informations
+ Filter stocks under multiple conditions
+ Download filtered result as .csv file


### Backend:
+ Django(3.1)
    + customized User model, take email as login account
    + self-build password restrictions
    + customized warning message
+ social-auth-app-django
    + Facebook
    + Google
+ bokeh
    + interactive plot legend

### Frontend:
+ Bootstrap
+ HTML
+ CSS
+ JavaScript

### Database:
+ PostgreSQL

## Setup

### 1. Enviroment
+ `pipenv --python 3.7`
+ `pipenv install -r requirements.txt`
+ `pipenv shell`
+ `set DJANGO_SETTINGS_MODULE=config.dev_settings`

### 2. Tables Build up
+ `python manage.py makemigraions accounts`
+ `python manage.py makemigraions info`
+ `python manage.py migrate`

### 3. Create demo data and run
+ `python manage.py dbshell`
+ `.read demodata/buildDemoData.sql`
+ `.quit`
+ `python manage.py runserver`

### 4. Visit
+ `https://127.0.0.1:8000`

## Note
+ if you need access to admin page, execute the command below to create superuser(admin account).Then visit `https://127.0.0.1:8000/admin`.

`python manage.py createsuperuser`

+ `set DJANGO_SETTINGS_MODULE=config.dev_settings` needs to be execute each time when restarting porject.
