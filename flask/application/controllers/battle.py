from flask import session, g, request
from application import app
from application.lib.auth import *
from application.models import battle_management, user_management
from application.models import battle_management, code_management
from application.models import battle_management, ship_management
from application.lib.game import game
from application.constants import *
from json import loads

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
    
    

def new_league(schoolId):
    query = "INSERT INTO league (schoolId) VALUES ('"+str(schoolId)+"')"
    res = insert_query(query)
    leagueId = res.connection.insert_id()

    where = "WHERE schoolId = '"+str(schoolId)+"' AND userLevel == 1"
    users  = get_users(where)

    userList = []

    for user in users:
        userData = {}
        userData[KEY_USER_ID] = user[COL_ID]
        userData[KEY_AI_MODULE] = get_latest_code(userData[KEY_USER_ID])
        userData[KEY_SHIP_PLACEMENT] = get_last_placement(userData[KEY_USER_ID])
        


    for user1 in userList:
        for user2 in userList:
            battle(user1,user2)


def battle(user1, user2):
    resultLog = game(
            loads(user1[KEY_SHIP_PLACEMENT]),
            loads(user2[KEY_SHIP_PLACEMENT]),
            user1[KEY_AI_MODULE],
            user2[KEY_AI_MODULE]
        ).get_log(False)
    
    insert_result(resultLog)
    






