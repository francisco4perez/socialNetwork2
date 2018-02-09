__authors__ = 'Jean-Baptiste Leprince and Francisco Perez'
import sqlite3
from flask import g



DATABASE = 'database.db'

# connect the database
def connect_db():
    g.db = sqlite3.connect(DATABASE)

#close the database
def close_db():
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#Insert a new user in the database 
def insert_user(email,password,token,firstname, familyname, gender,city,country):
    result = []
    try:
		#prepare statement to insert values in the users table
        cur = g.db.execute("insert into users values(?,?,?,?,?,?,?,?)", [email,password,token,firstname, familyname, gender,city,country])
        g.db.commit()
        return True
    except:
        return False

#get all the informations about a user depending of his token or email
def get_user(email,token):
    result = []
    # prepare statement to get values depending of the email and the token
    cursor = g.db.execute("select * from users where email = ? and token = ?", [email, token])
    rows = cursor.fetchall()
    cursor.close()
    
    for index in range(len(rows)):
        result.append({'email':rows[index][0], 'token':rows[index][2], 'firstname':rows[index][3],'familyname':rows[index][4],'gender':rows[index][5],'city':rows[index][6],'country':rows[index][7]})
    return result


def get_messages(email):
    result = []
    # comment
    cursor = g.db.execute("select * from messages where user_id = ?",email)
    rows = cursor.fetchall()
    cursor.close()
    # commment
    for index in range(len(rows)):
        result.append({"writer_id":rows[index][2], "content":rows[index][3]})
    return result