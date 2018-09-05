import json
import logging
import logging.handlers
from functools import wraps
from flask import jsonify
from flask import request
import os
import constants as cts
import datetime
import redis
from flask import current_app as curapp


__author__ = 'hughson.simon@gmail.com'

if not os.path.exists("logs/"):
    os.makedirs("logs/")
log_file = 'logs/user_management.log'


logging.basicConfig(level=logging.INFO,
                    filename=log_file,
                    format="%(asctime)s - %(name)s - %(message)s",
                    datefmt="%H:%M:%S",
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        # Do something with your request here
        try:
            request.get_json()
        except:
            msg = "payload must be a valid json"
            return (jsonify({'response_status': cts.RESPONSE_ERROR,
                              'response_message': msg}), 400)
        return f(*args, **kw)
    return wrapper

def  validate_registration_input(**data):
    """Validate if given input has mandatory keys"""
    MANDATORY_KEYS = ['email', "first_name", "last_name"]
    if all(k in data.keys() for k in MANDATORY_KEYS):
        #if MANDATORY_KEYS in data.keys():# check mandatory keys
        return True, "SUCCESS"
    else:
        return False, ("Mandatory fields Not Provided")


def  validate_group_create_input(**data):
    """Validate if given input has mandatory keys"""
    MANDATORY_KEYS = ['group_name']
    if all(k in data.keys() for k in MANDATORY_KEYS):
        return True, "SUCCESS"
    else:
        return False, ("Mandatory fields Not Provided")
