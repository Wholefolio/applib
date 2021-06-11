# Applib - toolbox for applications
Here we have a collection of tools for Wholefolio applications in python and django

## generate_secret_key
A python executable script for generating a random 50 character long key for use with Django's SECRET_KEY. The function generate can be imported directly to django

## Manager
A class that can be inherited to provide incoming socket capabilities for an application

## Healthcheck
A basic healthcheck view for use in Django applications

## Log
Logging tools for django. Here we have a logging filter for filtering out healthchecks from the log


## Tools
Additional functions
* bool_eval - evaluate a string to python boolean type
* get_db_details_postgres - get Django database details for PostgreSQL from environmental variables
* appRequest - wrapper around requests with logging
