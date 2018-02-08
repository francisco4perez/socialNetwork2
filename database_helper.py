__author__ = 'Sahand Sadjadee'
import sqlite3
from flask import g



DATABASE = 'database.db'


def connect_db():
    g.db = sqlite3.connect(DATABASE)

def close_db():
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def insert_contact(firstname, familyname, mobile):
    result = []

    try:
        cur = g.db.execute("insert into contact values(?,?,?)", [firstname, familyname, mobile])
        g.db.commit()
        return True
    except:
        return False

def get_contact(firstname, familyname):
    result = []
    cursor = g.db.execute("select * from contact where firstname = ? and familyname = ?", [firstname, familyname])
    rows = cursor.fetchall()
    cursor.close()
    for index in range(len(rows)):
        result.append({'firstname':rows[index][0], 'familyname':rows[index][1], 'mobile':rows[index][2]})
    return result






