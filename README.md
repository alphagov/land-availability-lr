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

Make sure the correct Heroku buildpacks are set:

```
heroku buildpacks:set https://github.com/cyberdelia/heroku-geo-buildpack.git
heroku buildpacks:set heroku/python
```

## Dump DB

You may need a newer version of psql - it must be the same or newer than the postgres version of the db. To get psql 9.6 on Ubuntu 16.04:

    sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    sudo apt-get install postgresql-client-9.6

To do the dump:

    pg_dump -W -h <db-host> -p 5432 -d landavailability-lr -U landavailability -F c -b -v -f lr.pg_dump

## Restore DB

TODO

# Python

The project is being developed and tested with **Python >= 3.5.x**
