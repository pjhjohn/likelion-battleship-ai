from application.const import *
import json, battleship_db

def add_fleet(user_id, placement) :
	query = "INSERT INTO shipPlacement (userId,placement) VALUES " + "('%s','%s')" % (str(user_id), placement)
	return battleship_db.insert(query)

def get_fleets(user_id, is_latest = False):
    query = "SELECT * FROM shipPlacement WHERE userId = '" + str(user_id)+"' ORDER BY uploadedTime DESC" + ['',' LIMIT 1'][is_latest]
    return select_query(query)

def get_latest_fleet(user_id):
    return json.loads(get_fleets(user_id, True)[0][Col.PLACEMENT])
