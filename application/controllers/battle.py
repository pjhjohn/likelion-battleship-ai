from flask import session, g, request, render_template
from application import app
from application.const import *
from application.lib.auth import *
from application.lib.game import game
from application.models import battleship_db, battle_manager, code_manager, fleet_manager, user_manager
import json

@app.route('/league', methods = ['POST'])
def league() :
    if not is_login() : return '1'
    if not session[Key.SCHOOL_ID] : return '1'
    new_league(session[Key.SCHOOL_ID])
    return '0'

@app.route('/get_battle_list', methods = ['POST'])
def get_battle_list() :
    league_id = request.form[Key.LEAGUE_ID]
    winner_id = request.form[Key.WINNER_ID]
    return json.dumps(battle_manager.get_battle_list(league_id, winner_id))

@app.route('/visualize', methods = ['GET', 'POST'], defaults = {'battle_id' : 0})
@app.route('/visualize/<battle_id>', methods = ['GET', 'POST'])
def visualize(battle_id) :
    if request.method == 'POST' :
        game_log = request.form['log']
    else :
        log_file = open('%s/%d.json' % (Path.LOGS, int(battle_id)))
        game_log = log_file.read()
        log_file.close()
    return render_template('visualize.html', log = game_log)

def new_league(school_id) :
    query = "INSERT INTO league (school_id) VALUES ('%d')" % school_id
    cursor = battleship_db.insert(query)
    league_id = cursor.connection.insert_id()

    where = "WHERE school_id = '%d' AND user_level = 1" % school_id
    users = user_manager.get_users(where)

    user_list = []
    for user in users :
        if user[Col.USER_LEVEL] > 1 : continue

        user_data = {}
        user_data[Key.USER_ID] = user[Col.ID]
        user_data[Key.AI_MODULE] = code_manager.get_latest_code_module(user_data[Key.USER_ID])
        user_data[Key.FLEET_DEPLOYMENT] = fleet_manager.get_latest_fleet(user_data[Key.USER_ID])
        if not user_data[Key.AI_MODULE] or not user_data[Key.FLEET_DEPLOYMENT] :
            continue
        user_list.append(user_data)

    for player1 in user_list :
        for player2 in user_list :
            if player1[Key.USER_ID] == player2[Key.USER_ID] :
                continue
            execute_battle(league_id, player1, player2)

def execute_battle(league_id, player1, player2) :
    result_log = game.play(player1[Key.FLEET_DEPLOYMENT], player2[Key.FLEET_DEPLOYMENT], player1[Key.AI_MODULE], player2[Key.AI_MODULE]).get_log(False)
    battle_manager.insert_result(league_id, player1[Key.USER_ID], player2[Key.USER_ID], result_log)