from flask import redirect, url_for, session, render_template, request
from application import app
from application.models.code_management import *
from application.lib.auth import *
from glob import glob
from application.constants import *


@app.route('/code')
def code():
    if not is_login():
        return redirect(url_for('login'))


    codes = get_codes(session[KEY_USER_ID])
    return render_template('code.html', current = request.path[1:],files=codes, filecount = len(codes))


@app.route('/submit_code', methods = ["POST"])
def submit_code():
    if not is_login():
        return '1'

    add_code(session[KEY_USER_ID],request.form['new'])
    

    # code test here

    if request.referrer and request.referrer.split('/')[-1] == 'test':
        return '0'
    return redirect(url_for('code'))