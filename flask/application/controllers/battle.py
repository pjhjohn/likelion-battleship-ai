from flask import session, g, request
from application import app
from application.lib.auth import *
from application.models import database, battle_management, code_management, ship_management, user_management
from application.lib.game import game
from application.constants import *
from json import loads, dumps

@app.route('/league', methods = ['POST'])
def league():
    if not is_login():
        return '1'

    schoolId = session[KEY_SCHOOL_ID]

    if not schoolId:
        #error
        return '1'
    else:
        new_league(schoolId)
        return '0'
    

@app.route('/get_battle_list', methods = ['POST'])
def get_battle_list():
    leagueId = request.form[KEY_LEAGUE_ID]
    winnerId = request.form[KEY_WINNER_ID]


    return dumps(battle_management.get_battle_list(leagueId, winnerId))

    

def new_league(schoolId):
    query = "INSERT INTO league (schoolId) VALUES ('"+str(schoolId)+"')"
    res = database.insert_query(query)
    leagueId = res.connection.insert_id()

    where = "WHERE schoolId = '"+str(schoolId)+"' AND userLevel = 1"
    users  = user_management.get_users(where)



    userList = []


    for user in users:
        if user[COL_USER_LEVEL] > 1:
            continue

        userData = {}
        userData[KEY_USER_ID] = user[COL_ID]
        userData[KEY_AI_MODULE] = code_management.get_latest_code(userData[KEY_USER_ID])
        userData[KEY_SHIP_PLACEMENT] = ship_management.get_last_placement(userData[KEY_USER_ID])
        userList.append(userData)
        


    for user1 in userList:
        for user2 in userList:
            if user1[KEY_USER_ID] != user2[KEY_USER_ID]:
                battle(leagueId, user1,user2)



def battle(leagueId, user1, user2):
    resultLog = game.game(
            user1[KEY_SHIP_PLACEMENT],
            user2[KEY_SHIP_PLACEMENT],
            user1[KEY_AI_MODULE],
            user2[KEY_AI_MODULE]
        ).get_log(False)
    
    battle_management.insert_result(leagueId, user1[KEY_USER_ID], user2[KEY_USER_ID], resultLog)
    






