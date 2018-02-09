from flask import app, request
from flask import Flask
import database_helper
import json

app = Flask(__name__)
app.debug = True


@app.before_request
def before_request():
    database_helper.connect_db()

@app.teardown_request
def teardown_request(exception):
    database_helper.close_db()


@app.route('/')
def main():
    return app.send_static_file('hello_world.html')

@app.route('/signin', methods=['POST'])
def signin_user():
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = database_helper.get_user_by_password(email, password)
    if result == True:
        return 'User signed in', 200
    else:
        return 'Authentification failed', 501


if __name__ == '__main__':
    app.run()

'''
@app.route('/')
@app.route('/save')
def save():
    return app.send_static_file('ui_save.html')



@app.route('/search')
def search():
    return app.send_static_file('ui_search.html')



@app.route('/savecontact', methods=['POST'])
def save_contact():




    firstname = request.get_json()['firstname']
    familyname = request.get_json()['familyname']
    phonenumber = request.get_json()['mobile']

    result = database_helper.insert_contact(firstname, familyname, phonenumber)
    if result == True:
        return 'contact added', 200
    else:
        return 'could not add the contact', 501


@app.route('/getcontact/<firstname>/<familyname>', methods=['GET'])
def get_contact(firstname = None, familyname = None):
    if firstname != None and familyname != None:
        result = database_helper.get_contact(firstname, familyname)
        if len(result) == 0:
            return 'contact not found', 404
        else:
            return json.dumps(result), 200
    else:
        return "", 404
'''
