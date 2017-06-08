# land-availability-lr
Land Registry service for Land Availability Tool

# Continuous integration status

[![Travis-CI Status](https://secure.travis-ci.org/alphagov/land-availability-lr.png?branch=master)](http://travis-ci.org/#!/alphagov/land-availability-lr)
[![codecov](https://codecov.io/gh/alphagov/land-availability-lr/branch/master/graph/badge.svg)](https://codecov.io/gh/alphagov/land-availability-lr)

# PostgreSQL Setup

Make sure you have **PostgreSQL** (tested with 9.6) installed.

It's strongly suggested to use Postgres.app on OSX and to install all the other
tools and dependencies using **brew**.

## Create DB

```
createdb landavailability-lr
```

## Setup DB

```
workon landavailability-lr
cd land-availability-lr/landavailability
./manage.py migrate
```

# Project Configuration

Make sure you have this environment variable set:

```
DATABASE_URL=postgres://USERNAME:PASSWORD@HOST:PORT/DBNAME
SECRET_KEY=abcd1234
```

example:

```
DATABASE_URL=postgres://andreagrandi@localhost:5432/landavailability-lr
SECRET_KEY=abcd1234
```

If you are using a Python virtual environment, you can save these values in
$venv_folder/bin/postactivate script:

```
export DATABASE_URL=postgres://andreagrandi@localhost:5432/landavailability-lr
export SECRET_KEY=abcd1234
```

## Dump DB

You may need a newer version of psql - it must be the same or newer than the postgres version of the db. To get psql 9.6 on Ubuntu 16.04:

    sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install postgresql-client-9.6

To do the dump:

    pg_dump -W -h <db-host> -p 5432 -d landavailability-lr -U landavailability -F c -b -v -f lr.pg_dump


# Importing data (monthly delta)

## User and token

To import LR delta data you need a user and token. First open a shell:

    workon landavailability-lr
    cd land-availability-lr/landavailability
    ./manage.py shell

In the shell:

```
# check if there is already an admin user
from django.contrib.auth.models import User
from django.db.models import Q
User.objects.filter(Q(is_superuser=True)).distinct()

# create admin user
user = User.objects.create_user('admin', password='pass', is_staff=True)
user.save()

# check if a token exists for this user
from rest_framework.authtoken.models import Token
Token.objects.filter(Q(user=user))

# create token
token = Token.objects.create(user=user)
print(token.key)
```

This prints the hex token e.g. `8f3f29c458d38a1b073992421965a15e90bd8db9`

## Get data

The LR data is not public.

## Run LR app

    workon landavailability-lr
    cd land-availability-lr/landavailability
    ./manage.py runserver localhost:8001

## Run import script

(while LR app runs in another shell)

TODO
