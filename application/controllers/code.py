from flask import redirect, url_for, render_template, request
from application import app
from application.const import *
from application.lib.auth import *
from application.models import code_manager

@app.route('/code')
def code() :
    if not is_login() :
        return redirect(url_for('login'))
    codes = code_manager.get_codes(session[Key.USER_ID])
    return render_template('code.html', current = request.path[1:], files = codes, file_count = len(codes), errormsg = ErrorMsg.CodeSubmit)

@app.route('/submit_code', methods = ['POST'])
def submit_code() :
    if not is_login() :
        return '1'
    # With Code Test
    code_manager.add_code(session[Key.USER_ID], request.form['new'])
    if request.referrer and request.referrer.split('/')[-1] == 'test' :
        return '0'
    return redirect(url_for('code'))