from database import *
from application.constants import *
from json import dumps

def get_school_id(leagueId):
    query = "SELECT schoolId FROM league WHERE ID = '"+str(leagueId)+"'"
    try:
        return select_query(query)[0][COL_SCHOOL_ID]
    except:
        return 0

def insert_result(uid1, uid2, log):
    winner = log[-1][KEY_PLAYER]
    query = "INSERT INTO battleResult (userId1, userId2, winnerId, log VALUES ('"+str(uid1)+"','"+str(uid2)+"','"+str(uid1 if winner == 1 else uid2)+"','"+escape(dumps(log))+"')"
    insert_query(query)
    