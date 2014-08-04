from database import *
from application import app
import sys
import os.path
from json import dumps




def email_duplicated(email):
    query = "SELECT ID FROM users WHERE email = '"+email+"'"
    if get_count(query):
        return True
    else:
        return False

def add_user(email, password, schoolId, members):
    salt = app.config['SALT']
    #members = map(lambda x:escape(x),members)
    
    query = "INSERT INTO users (email, password, schoolId) VALUES ('"+email+"',password('"+password+salt+"'), '"+schoolId+"')"
    
    res = insert_query(query)
    userId = res.connection.insert_id()

    query = "INSERT INTO teamMembers (userId, memberName) VALUES "
    for member in members:
        query += "('"+str(userId)+"','"+member+"'),"
    return insert_query(query[:-1])

def get_users(where):
    query = "SELECT * FROM users u LEFT JOIN (SELECT userId,GROUP_CONCAT(memberName) members FROM teamMembers GROUP BY userId) t ON u.ID = t.userId "+where
    return select_query(query)


