# python-django-stock
Stock information provider. There are fifty stocks, components of 0050.TW, contained in `demodata` folder.

## Update Record
2021.05.07 | Optimize pick_view, correct few misspelling
2021.04.25 | First Push

## Project Overview
### Screenshots

- Homepage

![](https://github.com/ycy-tw/python-django-stock/blob/7f2d2d79dbacc5f1488bb99164cdb18400749792/screenshots/hompage.png)

- Register

![](https://github.com/ycy-tw/python-django-stock/blob/7fa715f8555951abd9cc24067ccad6439bc6a4af/screenshots/register.png)

- Login & Third-Party Connect (Facebook and Google)

![](https://github.com/ycy-tw/python-django-stock/blob/b6a658fc7e3fffbc19bd1efe5c346527ff512726/screenshots/login.png)

- Forgot Password

![](https://github.com/ycy-tw/python-django-stock/blob/b6a658fc7e3fffbc19bd1efe5c346527ff512726/screenshots/forgot_pwd.png)

- Search

![](https://github.com/ycy-tw/python-django-stock/blob/b6a658fc7e3fffbc19bd1efe5c346527ff512726/screenshots/search.png)

- Basic Stock Information

![](https://github.com/ycy-tw/python-django-stock/blob/b6a658fc7e3fffbc19bd1efe5c346527ff512726/screenshots/basic_info.png)

- Chips Stock Information

![](https://github.com/ycy-tw/python-django-stock/blob/b6a658fc7e3fffbc19bd1efe5c346527ff512726/screenshots/chips_info.png)

- Stock Picking

![](https://github.com/ycy-tw/python-django-stock/blob/b6a658fc7e3fffbc19bd1efe5c346527ff512726/screenshots/pick.png)

- Stock Picking Result

![](https://github.com/ycy-tw/python-django-stock/blob/b6a658fc7e3fffbc19bd1efe5c346527ff512726/screenshots/pick_result.png)


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

### 2. Tables Build up
+ `python manage.py makemigrations accounts`
+ `python manage.py makemigrations info`
+ `python manage.py migrate`

### 3. Create demo data and run
+ `python demodata/add_demo_data.py`
+ `python manage.py runserver`

### 4. Visit
+ `https://127.0.0.1:8000`

## Note
+ if you need access to admin page, execute the command below to create superuser(admin account).Then visit `https://127.0.0.1:8000/admin`.

`python manage.py createsuperuser`
