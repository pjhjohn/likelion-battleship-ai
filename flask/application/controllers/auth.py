from flask import request, redirect, url_for, session, render_template
from application import app
from application.lib.auth import *
from application.models.user_management import *
from application.models.database import select_query
from application.constants import *


@app.route('/join', methods = ['POST'])
def join():
    salt = app.config['SALT']
    email = request.form[KEY_EMAIL]
    schoolId = request.form[KEY_SCHOOL_ID]
    password = request.form[KEY_PASSWORD]
    members = []
    for i in range(1,4):
        if KEY_MEMBERS + str(i) in request.form:
            members.append(request.form[KEY_MEMBERS+str(i)].encode('utf8'))

    if email_duplicated(email):
        # duplicated email
        return '1'
    else:
        # insert to db
        add_user(email,password,schoolId, members)
        return '0'

@app.route('/join_submit',methods = ['POST'])
def join_submit():
    return str(request.form)

@app.route('/login')
def login():
    if is_login():
        return redirect(url_for('index'))

    query = "SELECT * FROM schoolList"
    res = select_query(query)

    return render_template('login.html',schoolList = res)

@app.route('/login_submit', methods=['POST'])
def login_submit():
    email = request.form[KEY_EMAIL]
    password = request.form[KEY_PASSWORD]+app.config['SALT']
    where = "WHERE email = '"+email+"' AND password = password('"+password+"')"
    res = get_users(where)
    if len(res) == 1:
        row = res[0]
        session[KEY_USER_ID] = row[COL_ID]
        session[KEY_USER_LEVEL] = row[COL_USER_LEVEL]
        session[KEY_SCHOOL_ID] = row[COL_SCHOOL_ID]
        return '0'
    else:
        #fail
        return '1'

@app.route('/logout')
def logout():
    session.pop(KEY_USER_ID,None)
    session.pop(KEY_USER_LEVEL,None)
    return redirect(url_for('login'))
