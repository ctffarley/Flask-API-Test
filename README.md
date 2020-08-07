# Flask API Test

## Purpose
A basic Flask API that implements CRUD operations using Flask-RESTX and stores
data in a PostgreSQL server. Interaction with the database is done using
SQLAlchemy. Flask-RESTX also allows for the creation of swagger documentation
for the API.

## Setup

### Environment Variables
Copy the `.env-template` file, and rename the copy `.env`. This file will store
environent variables for configuring the API (these values will be assigned in
the sections below).

### Python Setup
Create a new virtual environment then run `_install_requirements` to pip install
the packages in `requirements.txt`. Store the name of your virtual environment
in the `.env` file as `VENV_NAME`.

### Postgres Setup
Specify the postgres configuration such as IP/domain, port, user, password, etc.
in `.env`. 

Once all environment varaibles have been set, run `source .env` in order to
export all environment variables

## Scripts
* `_activate_environment`
    * exports environment varaibles in `.env` and activates the virtual environment
    * _Important_: must be run like so: `. ./_activate-environment`

* `_export_requirements`
    * used to export current dependencies to `requirements.txt`

* `_install_requirements`
    * used to install all dependencies from `requirements.txt`
    * should be run inside the virtual environment

* `_start_dev_server`
    * starts the api