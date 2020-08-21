# Django Project Lily

A Django Rest API project for Online Pizza Shop Backend.

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

### Install dependencies & activate virtualenv

```
pip install virtualenv
virtualenv -p python3.8 venv
source venv/bin/activate
```


### Install requirements inside virtual environment:
```
pip install -r requirements
```

### Make a .env file and configure your necessary parameter(see env.example):

```
touch .env
```


### Apply migrations

```
python manage.py makemigrations
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