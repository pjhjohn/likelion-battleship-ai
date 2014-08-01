from database import *
from application.constants import *
from json import dump

def get_school_id(leagueId):
    query = "SELECT schoolId FROM league WHERE ID = '"+str(leagueId)+"'"
    try:
        return select_query(query)[0][COL_SCHOOL_ID]
    except:
        return 0

def insert_result(leagueId, uid1, uid2, log):
    winner = log[-1][KEY_PLAYER]
    query = "INSERT INTO battleResult (leagueId, userId1, userId2, winnerId) VALUES ('"+str(leagueId)+"','"+str(uid1)+"','"+str(uid2)+"','"+str(uid1 if winner == 1 else uid2)+"')"

    res = insert_query(query)
    battleResultId = res.connection.insert_id()
    logFile = open(LOGS_DIR + '/' + str(battleResultId)+'.json','w')
    
    dump(log,logFile)

    logFile.close()

def get_league_list(schoolId):
    query = "SELECT * FROM league l LEFT JOIN schoolList s ON l.schoolId = s.ID WHERE s.ID = '"+str(schoolId)+"' ORDER BY createdTime DESC"

    return select_query(query)

def get_ranking(leagueId):
    query = "SELECT * FROM (SELECT winnerId, count(*) winCount FROM battleResult WHERE leagueId = '"+str(leagueId)+"' GROUP BY winnerId) w LEFT JOIN users u ON w.winnerId = u.ID LEFT JOIN (SELECT userId, GROUP_CONCAT(memberName) teamMembers FROM teamMembers GROUP BY userId) t ON u.ID = t.userId ORDER BY winCount DESC"

    return select_query(query)


def get_battle_list(leagueId, winnerId):
    query = "SELECT * FROM battleResult b LEFT JOIN (SELECT userId, GROUP_CONCAT(memberName) teamMembers1 FROM teamMembers GROUP BY userId) u1 ON b.userId1 = u1.userId LEFT JOIN (SELECT userId, GROUP_CONCAT(memberName) teamMembers2 FROM teamMembers GROUP BY userId) u2 ON b.userId2 = u2.userId WHERE b.leagueId = '"+str(leagueId)+"' AND (b.userId1 = '"+str(winnerId)+"' OR b.userId2 = '"+str(winnerId)+"')"

    return select_query(query)


