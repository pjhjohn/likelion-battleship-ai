from database import *
from application.constants import *
from json import dump

def get_school_id(leagueId):
    query = "SELECT schoolId FROM league WHERE ID = '"+str(leagueId)+"'"
    try:
        return select_query(query)[0][COL_SCHOOL_ID]
    except:
        return 0

def insert_result(uid1, uid2, log):
    winner = log[-1][KEY_PLAYER]
    query = "INSERT INTO battleResult (userId1, userId2, winnerId) VALUES ('"+str(uid1)+"','"+str(uid2)+"','"+str(uid1 if winner == 1 else uid2)+"')"

    res = insert_query(query)
    battleResultId = res.connection.insert_id()
    logFile = open(LOGS_DIR + '/' + str(battleResultId)+'.json','w')
    
    dump(log,logFile)

    logFile.close()