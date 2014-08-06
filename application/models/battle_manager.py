from application.const import *
import json, battleship_db

def get_school_id(league_id) :
    query = "SELECT school_id FROM league WHERE ID = " + "'%d'" % league_id
    try    : return battleship_db.select(query)[0][Col.SCHOOL_ID]
    except : return 0

def insert_result(league_id, uid1, uid2, game_log) : 
    winner = game_log['history'][-1][Key.PLAYER]
    if not game_log['history'][-1][Key.SINK] :
        winner = [uid2, uid1][winner == 2]
    else :
        winner = [uid2, uid1][winner == 1]
    query = "INSERT INTO battle_result (league_id, user_id1, user_id2, winner_id) VALUES " + "('%d', '%d', '%d', '%d')" % (league_id, uid1, uid2, winner)
    cursor = battleship_db.insert(query)
    battle_result_id = cursor.connection.insert_id()
    with open('%s/%d.json'%(Path.LOGS, battle_result_id), 'w') as log_file :
        json.dump(game_log, log_file)

def get_battle_list(league_id, winner_id):
    query = "SELECT * FROM battle_result br LEFT JOIN (SELECT user_id, GROUP_CONCAT(member_name) team_members1 FROM team_members GROUP BY user_id) user1 ON br.user_id1 = user1.user_id LEFT JOIN (SELECT user_id, GROUP_CONCAT(member_name) team_members2 FROM team_members GROUP BY user_id) user2 ON br.user_id2 = user2.user_id WHERE br.league_id = '" + '%d'%league_id + "' AND (br.user_id1 = '" + '%d'%winner_id + "' OR br.user_id2 = '" + '%d'%winner_id + "')"
    return battleship_db.select(query)

def get_league_list(school_id) : 
    query = "SELECT * FROM league lg LEFT JOIN school_list sl ON lg.school_id = sl.ID WHERE sl.ID = '" + '%d'%school_id + "' ORDER BY createdTime DESC"
    return battleship_db.select(query)

def get_ranking(league_id):
    query = "SELECT * FROM (SELECT winner_id, count(*) win_count FROM battle_result WHERE league_id = '" + '%d'%league_id + "' GROUP BY winner_id) winner LEFT JOIN users user ON winner.winner_id = user.ID LEFT JOIN (SELECT user_id, GROUP_CONCAT(member_name) team_members FROM team_members GROUP BY user_id) team ON user.ID = team.user_id ORDER BY win_count DESC"
    return battleship_db.select(query)