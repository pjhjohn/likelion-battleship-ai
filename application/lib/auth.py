from flask import session
from application.constants import *

def is_login():
    return KEY_USER_ID in session and KEY_USER_LEVEL in session and KEY_SCHOOL_ID in session

def is_admin():
    return is_login() and int(session[KEY_USER_LEVEL]) > 1

