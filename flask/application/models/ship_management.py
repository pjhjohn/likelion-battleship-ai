from database import *
from application import app
from json import loads
from application.constants import *

def add_placement(userId, placement):

    query = "INSERT INTO shipPlacement (userId,placement) VALUES ('"+str(userId)+"','"+placement+"')"
    return insert_query(query)

def get_placements(userId, latest = False):
    query = "SELECT * FROM shipPlacement WHERE userId = '"+str(userId)+"' ORDER BY uploadedTime DESC"
    if latest:
        query += " LIMIT 1"
    return select_query(query)

def get_last_placement(userId):
    return loads(get_placements(userId,True)[0][COL_PLACEMENT])
