# land-availability-lr
Land Registry service for Land Availability Tool

# Continuous integration status

[![Travis-CI Status](https://secure.travis-ci.org/alphagov/land-availability-lr.png?branch=master)](http://travis-ci.org/#!/alphagov/land-availability-lr)

# PostgreSQL Setup

Make sure you have **PostgreSQL** (tested with 9.6) installed and also PostGIS.

It's strongly suggested to use Postgres.app on OSX (which includes PostGIS) and
to install all the other tools and dependencies using **brew**.


postgres -D /usr/local/var/postgres &

## Create DB

```
createdb landavailability-lr
```

# Project Configuration

Make sure you have these environment variable set:

```
DATABASE_URL=postgres://USERNAME:PASSWORD@HOST:PORT/DBNAME
SECRET_KEY=abcd1234
OPBEAT_ORGANIZATION_ID=abcd1234
OPBEAT_APP_ID=abcd1234
OPBEAT_SECRET_TOKEN=abcd1234
OPBEAT_DISABLE_SEND=true
```

If you are using a Python virtual environment, you can save these values in
$venv_folder/bin/postactivate script e.g.:

```
export DATABASE_URL=postgres://andreagrandi@localhost:5432/landavailability-lr
export SECRET_KEY=abcd1234
export OPBEAT_ORGANIZATION_ID=abcd1234
export OPBEAT_APP_ID=abcd1234
export OPBEAT_SECRET_TOKEN=abcd1234
export OPBEAT_DISABLE_SEND=true
```

# Python

The project is being developed and tested with **Python >= 3.5.x**

# Tests

To run the tests:
```
OPBEAT_DISABLE_SEND=true py.test
```