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
def insert_user(email,password,token,firstname, familyname, gender,city,country,salt):
    result = []
    try:
		#prepare statement to insert values in the users table
        cur = g.db.execute("insert into users values(?,?,?,?,?,?,?,?,?,null)", [email,password,token,firstname, familyname, gender,city,country,salt])
        g.db.commit()
        return True
    except:
        return False

#update the token of the user with the corresponding address
def update_token(token,email):
    try:
        #prepare statement to insert new token
        cur = g.db.execute("update users set token = ? where email = ?", [token, email])
        g.db.commit()
        return True
    except:
        return False

#delete the token of the user with the corresponding address
def delete_token(token):
    try:
        cur = g.db.execute("update users set token = '' where token = ?", [token])
        g.db.commit()
        cur.close()
        return True
    except:
        return False

def get_token_by_email(email):
    cursor = g.db.execute("select * from users where email = ?", [email])
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) != 0:
        user = rows[0]
        token = user[2]
        return token
    return ""


#delete the token of the user with the corresponding address
def delete_token_by_email(email):
    try:
        cur = g.db.execute("update users set email = '' where email = ?", [email])
        g.db.commit()
        cur.close()
        return True
    except:
        return False

#update the password in the database
def update_password(token,oldPassword,newPassword):
    user = get_user_by_token(token)[0]
    query = g.db.execute("update users set password = ? where token = ?",[newPassword,token])
    g.db.commit()
    query.close()
    return True

#get all information about a user depending of his token
def get_user_by_token(token):
    result = []
    cursor = g.db.execute("select * from users where token = ?",[token])
    rows = cursor.fetchall()
    cursor.close()
    if rows ==[]:
        return None
    d = {}
    d["email"],d["firstname"],d["familyname"],d["gender"],d["city"],d["country"] = rows[0][0],rows[0][3],rows[0][4],rows[0][5],rows[0][6],rows[0][7]
    return d

#get all information about a user depending of his email
def get_user_by_email(email):
    result = []
    # prepare statement to get values depending of the email and the token
    cursor = g.db.execute("select * from users where email = ?", [email])
    rows = cursor.fetchall()
    cursor.close()
    d = {}
    if rows:
        d["email"],d["firstname"],d["familyname"],d["gender"],d["city"],d["country"] = rows[0][0],rows[0][3],rows[0][4],rows[0][5],rows[0][6],rows[0][7]
    #for index in range(len(rows)):
        #result.append({'email':rows[index][0], 'firstname':rows[index][3],'familyname':rows[index][4],'gender':rows[index][5],'city':rows[index][6],'country':rows[index][7]})
    return d

#get all information about a user depending of his email and password
def get_user_by_email_and_password(email,password):
    result = []
    # prepare statement to get values depending of the email and the token
    cursor = g.db.execute("select * from users where email = ? and password = ?", [email,password])
    rows = cursor.fetchall()
    cursor.close()
    if not rows:
        return None
    d = {}
    d["email"],d["firstname"],d["familyname"],d["gender"],d["city"],d["country"] = rows[0][0],rows[0][3],rows[0][4],rows[0][5],rows[0][6],rows[0][7]
    return d

#get the salt of a given password
def get_salt_by_email(email):
    result=[]
    # prepare statement to get the salt depending of the email
    cursor = g.db.execute("select salt from users where email = ?", [email])
    rows = cursor.fetchall()
    cursor.close()
    if not rows:
        return None
    d = {}
    d["salt"]= rows[0][0]
    return d

#get all messages of a profile given his email
def get_messages(email):
    result = []
    # prepare statement to get all the messages corresponding to this email
    cursor = g.db.execute("select * from messages where user_id = ?",[email])
    rows = cursor.fetchall()
    cursor.close()
    # append all the messages
    for index in range(len(rows)):
        result.append({"id":rows[index][0],"writer_id":rows[index][2], "content":rows[index][3]})
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

#delete a message on a profile with the specified content and writer
def delete_message(id):
    try:
        #prepare statement to insert values in the messages table
		cur = g.db.execute("delete from messages where id = ?", [id])
		g.db.commit()
		return True
    except:
        return False

def post_profilepicture(token,image):
    try:
		#prepare statement to change the profile picture of a user
		cur = g.db.execute("update users set profilepicture = ? where token = ?", [image,token])
		g.db.commit()
		return True
    except:
        return False
