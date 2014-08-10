from application.const import *
import json, battleship_db

def add_fleet(user_id, deployment) :
	query = "INSERT INTO fleet_deployment (user_id, deployment) VALUES " + "('%d','%s')" % (user_id, deployment)
	return battleship_db.insert(query)

def get_fleets(user_id, is_latest = False):
    query = "SELECT * FROM fleet_deployment WHERE user_id = '%d' ORDER BY uploaded_time DESC%s" % (user_id , ['',' LIMIT 1'][is_latest])
    return battleship_db.select(query)

def get_latest_fleet(user_id):
	fleets = get_fleets(user_id, True)
	if len(fleets) > 0 :
		return json.loads(fleets[0][Col.DEPLOYMENT])
	else : 
		return None
		#raise ValueError('AT LEAST ONE FLEET DEPLOYMENT IS NEEDED')
	# AT LEAST ONE FLEET DEPLOYMENT IS NEEDED
