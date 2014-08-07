from flask import session
from application.const import *

def is_login():
    return Key.USER_ID in session and Key.USER_LEVEL in session and Key.SCHOOL_ID in session

def is_admin():
    return is_login() and int(session[Key.USER_LEVEL]) > 1

