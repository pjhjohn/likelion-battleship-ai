from application.const import *
import json, battleship_db

def get_school_id(league_id) :
    query = "SELECT school_id FROM league WHERE ID = " + "'%d'" % league_id
    try    : return battleship_db.select(query)[0][Col.SCHOOL_ID]
    except : return 0

def insert_result(league_id, player1_id, player2_id, game_log) : 
    winner_id = game_log['history'][-1][Key.PLAYER]
    if not game_log['history'][-1][Key.SINK] : 
        winner_id = [player2_id, player1_id][winner_id == 2]
    else :
        winner_id = [player2_id, player1_id][winner_id == 1]
    query = "INSERT INTO battle_result (league_id, player1_id, player2_id, winner_id) VALUES " + "('%d', '%d', '%d', '%d')" % (league_id, player1_id, player2_id, winner_id)
    cursor = battleship_db.insert(query)
    battle_result_id = cursor.connection.insert_id()
    with open('%s/%d.json'%(Path.LOGS, battle_result_id), 'w') as log_file :
        json.dump(game_log, log_file)

def get_battle_list(league_id, winner_id):
    query = "SELECT * FROM battle_result b_result LEFT JOIN (SELECT user_id, GROUP_CONCAT(member_name) member1 FROM team_member GROUP BY user_id) player1 ON b_result.player1_id = player1.user_id LEFT JOIN (SELECT user_id, GROUP_CONCAT(member_name) member2 FROM team_member GROUP BY user_id) player2 ON b_result.player2_id = player2.user_id WHERE b_result.league_id = '%d' AND (b_result.player1_id = '%d' OR b_result.player2_id = '%d')" % (league_id, winner_id, winner_id)
    return battleship_db.select(query)

def get_league_list(school_id) : 
    query = "SELECT * FROM league lg LEFT JOIN school_list sl ON lg.school_id = sl.ID WHERE sl.ID = '%d' ORDER BY created_time DESC" % school_id
    return battleship_db.select(query)

def get_ranking(league_id):
    query = "SELECT * FROM (SELECT winner_id, count(*) win_count FROM battle_result WHERE league_id = '%d' GROUP BY winner_id) winner LEFT JOIN user usr ON winner.winner_id = usr.ID LEFT JOIN (SELECT user_id, GROUP_CONCAT(member_name) members FROM team_member GROUP BY user_id) team ON usr.ID = team.user_id ORDER BY win_count DESC" % league_id
    return battleship_db.select(query)