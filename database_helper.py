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

#update the token of the user with the corresponding address
def update_token(token,email):
    result = []
    try:
        #prepare statement to insert new token 
        cur = g.db.execute("update users set token = ? where email = ?", [token, email])
        g.db.commit()
        return True
    except:
        return False

#Change the password in the database
def change_password(token,oldPassword,newPassword):
    user = get_user_by_token(token)[0]
    print user["email"]
    print newPassword
    query = g.db.execute("update users set password = ? where token = ?",[newPassword,token])
    g.db.commit()
    query.close()
    return "Changed!"

#get all information about a user depending of his token
def get_user_by_token(token):
    result = []
    cursor = g.db.execute("select * from users where token = ?",[token])
    rows = cursor.fetchall()
    cursor.close()
    for index in range(len(rows)):
        result.append({'email':rows[index][0], 'firstname':rows[index][3],'familyname':rows[index][4],'gender':rows[index][5],'city':rows[index][6],'country':rows[index][7]})
    return result

#get all information about a user depending of his email
def get_user_by_email(email):
    result = []
    # prepare statement to get values depending of the email and the token
    cursor = g.db.execute("select * from users where email = ?", [email])
    rows = cursor.fetchall()
    cursor.close()
    for index in range(len(rows)):
        result.append({'email':rows[index][0], 'firstname':rows[index][3],'familyname':rows[index][4],'gender':rows[index][5],'city':rows[index][6],'country':rows[index][7]})
    return result

#get all information about a user depending of his email and password
def get_user_by_email_and_password(email,password):
    result = []
    # prepare statement to get values depending of the email and the token
    cursor = g.db.execute("select * from users where email = ? and password = ?", [email,password])
    print 'hello'
    rows = cursor.fetchall()
    cursor.close()
    for index in range(len(rows)):
        result.append({'email':rows[index][0],'password':rows[index][1], 'firstname':rows[index][3],'familyname':rows[index][4],'gender':rows[index][5],'city':rows[index][6],'country':rows[index][7]})
    return result

#get all messages of a profile given his email
def get_messages(email):
    result = []
    # prepare statement to get all the messages corresponding to this email
    cursor = g.db.execute("select * from messages where user_id = ?",[email])
    rows = cursor.fetchall()
    cursor.close()
    # append all the messages
    for index in range(len(rows)):
        result.append({"writer_id":rows[index][2], "content":rows[index][3]})
    return result

# insert a new message on the messages table with a content, a writer and and the current profile
def insert_message(user_id,writer, content):
    try:
		#prepare statement to insert values in the messages table
		cur = g.db.execute("insert into messages values(null,?,?,?)", [user_id,writer,content])
		g.db.commit()
		return True
    except:
        return False