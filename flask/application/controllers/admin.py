from flask import redirect, url_for, session, render_template, request
from application import app
from application.lib.auth import *
from application.models.user_management import *
from application.constants import *
from json import dumps,loads


@app.route('/admin')
def admin():
    if not is_login():
        return redirect(url_for('login'))
    if not is_admin():
        return redirect(url_for('index'))


    res = get_users("WHERE schoolId=(SELECT schoolId FROM users WHERE ID = '"+session[KEY_USER_ID]+"')" if int(session[KEY_USER_LEVEL]) < 3 else '')
    userList = []
    for user in res : 
        user[KEY_MEMBERS] = user[KEY_MEMBERS].decode('utf8')
        userList.append(user)

    
    return render_template('admin.html', current = request.path[1:],users = userList)


@app.route('/get_user_list', methods = ['POST'])
def get_user_list():
    schoolId = session[KEY_SCHOOL_ID]
    userLevel = session[KEY_USER_LEVEL]

    

    if not is_admin():
        return dumps([])
    else:
        query = "SELECT * FROM users u left join schoolList s ON u.schoolId = s.ID"

        if userLevel == LEVEL_SCHOOL_ADMIN:
            query += " WHERE s.schoolId = '"+str(schoolId)+"'"

        result = select_query(query)
        userList = []
        for user in result:
            user[KEY_MEMBERS] = ', '.join(loads(user[KEY_MEMBERS]))
            userList.append(user)
        return dumps(userList)

