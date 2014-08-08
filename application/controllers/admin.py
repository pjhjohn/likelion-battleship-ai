from flask import redirect, url_for, session, render_template, request
from application import app
from application.const import *
from application.lib.auth import *
from application.models import user_manager, battle_manager, battleship_db
import json

@app.route('/admin')
@app.route('/admin/<active>')
def admin(active = 'user_list') :
    if not is_login() :
        return redirect(url_for('login'))
    # Now Logged in
    if not is_admin() :
        return redirect(url_for('index'))
    # Now Logged in as ADMIN
    where = "WHERE school_id = (SELECT school_id FROM user WHERE ID = '%s')" % ['', str(session[Key.USER_ID])][int(session[Key.USER_LEVEL]) < 3]
    cursor = user_manager.get_users(where)
    user_list = []
    for user in cursor :
        user[Key.MEMBERS] = user[Key.MEMBERS].decode('utf-8')
        user_list.append(user)

    cursor = battle_manager.get_league_list(session[Key.SCHOOL_ID])
    league_list = []
    for row in cursor :
        row[Col.SCHOOL_NAME] = row[Col.SCHOOL_NAME].decode('utf-8')
        league_list.append(row)
    league_count = len(league_list)
    for i in range(league_count) :
        league_list[i][Key.RANKING] = battle_manager.get_ranking(league_list[i][Col.ID])

    return render_template('admin.html', current = request.path[1:], users = user_list, league_list = league_list, league_count = league_count, active = active if active else 'user_lst')

@app.route('/get_user_list', methods = ['POST'])
def get_user_list() :
    school_id = session[Key.SCHOOL_ID]
    user_level = session[Key.USER_LEVEL]

    if not is_admin() :
        return json.dumps([])
    else :
        query = "SELECT * FROM user usr LEFT JOIN school_list sl ON usr.school_id = sl.ID" + [''," WHERE sl.school_id = '%d'" % school_id][user_level==Level.SCHOOL_ADMIN]
        cursor = battleship_db.select(query)
        user_list = []
        for user in cursor :
            user[Key.MEMBERS] = ', '.join(json.loads(user[Key.MEMBERS]))
            user_list.append(user)
        return json.dumps(user_list)