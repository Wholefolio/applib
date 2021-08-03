import requests
import json
import simplejson
import logging
from os import environ
from django.core.exceptions import ImproperlyConfigured
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def bool_eval(value):
    """Evaluate a string value to python boolean True/False"""
    if not isinstance(value, str):
        return value
    if value.lower() in ["y", "t", "true", "yes"]:
        return True
    return False


def get_db_details_postgres():
    """Get the DB details from a env variables."""
    ENV_VARIABLES = ("DB_HOSTNAME", "DB_USERNAME", "DB_PASSWORD",
                     "DB_DATABASE")
    DATABASES = {}
    # We must have EACH env variable so that we can access the DB
    for i in ENV_VARIABLES:
        if i not in environ:
            raise ImproperlyConfigured(
                    "Missing mandatory enviromental variable {}".format(i))

    # Check for the DB port
    if "DB_PORT" in environ:
        db_port = environ.get("DB_PORT")
    else:
        db_port = "5432"

    DATABASES['default'] = {
                   "ENGINE": "django.db.backends.postgresql",
                   "NAME": environ.get("DB_DATABASE"),
                   "USER": environ.get("DB_USERNAME"),
                   "PASSWORD": environ.get("DB_PASSWORD"),
                   "HOST": environ.get("DB_HOSTNAME"),
                   "PORT": db_port}
    return DATABASES


def appRequest(method, url, data=None, retry=3):
    """Create a request to an app and return the result."""
    logger = logging.getLogger()
    HEADERS = {"Content-Type": "application/json"}
    resp = False
    retry_strategy = Retry(
        total=retry,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    try:
        resp = http.request(method, url, data=json.dumps(data), headers=HEADERS, timeout=3)
    except requests.exceptions.ConnectionError as e:
        msg = f"Can't connect to app! Error: {e}! Retries tried: {retry}"
        logger.critical(msg)
        return {"error": msg}
    except requests.exceptions.Timeout:
        msg = "Request timeout reached!"
        logger.critical(msg)
        return {"error": msg}
    except requests.exceptions.ChunkedEncodingError as e:
        msg = f"Connection broken. Error: {e}"
        logger.critical(msg)
        return {"error": msg}
    if not resp.ok:
        try:
            msg = "App request failed. Error: {}".format(resp.json())
            logger.debug(msg)
        except (json.decoder.JSONDecodeError, simplejson.errors.JSONDecodeError):
            msg = "App request failed. Error: {}".format(resp.text)
            logger.debug(msg)
        return {"error": msg}
    logger.debug({"message": "Got data from app:\n{}".format(resp.json())})
    return resp.json()
