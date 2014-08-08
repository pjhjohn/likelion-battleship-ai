from flask import request, redirect, url_for, session, render_template
from application import app
from application.const import *
from application.lib.auth import *
from application.models import user_manager, battleship_db

@app.route('/join', methods = ['POST'])
def join() :
    email     = request.form[Key.EMAIL]
    school_id = request.form[Key.SCHOOL_ID]
    password  = request.form[Key.PASSWORD]
    members   = [request.form[key].encode('utf-8') for key in ['%s%d'%(Key.MEMBERS, i) for i in [1,2,3]] if key in request.form]

    email_duplicated = user_manager.is_email_duplicated(email)
    if not email_duplicated : user_manager.add_user(email, password, school_id, members)
    return ['0', '1'][email_duplicated]

@app.route('/login')
def login() :
    if is_login() : return redirect(url_for('index'))
    query    = "SELECT * FROM school_list"
    cursor   = battleship_db.select(query)
    return render_template('login.html', school_list = cursor)

@app.route('/login_submit', methods = ['POST'])
def login_submit() :
    email    = request.form[Key.EMAIL]
    password = request.form[Key.PASSWORD] + app.config['SALT']
    where    = "WHERE email = '%s' AND password = password('%s')" % (email, password)
    cursor   = user_manager.get_users(where)

    if not len(cursor) == 1 : return '1'
    row = cursor[0]
    session[Key.USER_ID]    = row[Col.ID]
    session[Key.USER_LEVEL] = row[Col.USER_LEVEL]
    session[Key.SCHOOL_ID]  = row[Col.SCHOOL_ID]
    return '0'

@app.route('/logout')
def logout() :
    session.pop(Key.USER_ID   , None)
    session.pop(Key.USER_LEVEL, None)
    session.pop(Key.SCHOOL_ID , None)
    return redirect(url_for('login'))