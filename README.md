# Django Rest API Project

A Django Rest API project for Online Pizza Shop Backend.

## Technology:
* Core Language: Python 3.8
* Frameworks: Django 3.1, DRF 3.11.1
* Database: PostgreSQL 10.13

I think you have already install python v3.8 and postgreSQL v10.13 in your machine.

## Create PostgreSQL DB and User

Change to the PostgreSQL system user:
```
sudo su postgres
psql
```

#### Create a database for the project

```
CREATE DATABASE pizza;
```

#### Create a database user for the project:

```
CREATE USER mahfuz WITH PASSWORD 'bs23';
```

#### Give the new user access to administer the new database:

```
GRANT ALL PRIVILEGES ON DATABASE pizza TO bs23;
```

#### Exit out of the PostgreSQL user's shell session by typing:

```
\q
exit
```

### Clone the project

```
git clone https://github.com/mahfuz110244/pizza-shop-api.git
```

### Go to the project directory
```
cd pizza-shop-api/
```

### Install dependencies & activate virtualenv

```
pip install virtualenv
virtualenv -p python3.8 venv
source venv/bin/activate
```


### Install requirements inside virtual environment:
```
pip install -r requirements.txt
```

### Make a .env file and configure your necessary parameter(see env.example):

```
touch .env
```


### Apply migrations

```
python manage.py makemigrations user
python manage.py makemigrations shop
python manage.py migrate
```

### Running

### A development server for API

Just run this command:

```
python manage.py runserver
```

### Run API test scripts

Just run this command:

```
python manage.py test
```

### Create Superuser
Create superuser with phone number and password and consider superuser will be store managers of
the pizza shop.

```
python manage.py createsuperuser
```

### Login Admin Panel with phone number and password
Admin Panel URL
```
http://127.0.0.1:8000/admin
```