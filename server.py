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
    return app.send_static_file('client.html')

def verify_password(email, password):
    result = database_helper.get_user_by_email_and_password(email,password)
    try :
        if result:
            return True
        else :
            return False
    except:
        return False

@app.route('/signin', methods=['PUT'])
def sign_in():
    print "this is my request" + str(request)
    print request.get_json()
    email = request.get_json()['email']
    password = request.get_json()['password']
    if verify_password(email,password):
        return 'User signed in', 200
    else:
        return 'Authentification failed', 501

@app.route('/signup',methods=['PUT'])
def sign_up():
    try:
        email = request.get_json()['email']
        password = request.get_json()['password']
        firstname = request.get_json()['firstname']
        familyname = request.get_json()['familyname']
        gender = request.get_json()['gender']
        city = request.get_json()['city']
        country = request.get_json()['country']
        if len(email)!=0 and len(password)>=6 and len(firstname)!=0 and len(familyname)!=0 and len(gender)!=0 and len(city)!=0 and len(country)!=0 :
            exist = database_helper.get_user_by_email(email)
            if exist:
                return 'User signed up', 200
        else:
            return 'Authentification failed', 501
    except:
        return 'Not enough parameters',404


@app.route('/getdatabytoken/<token>', methods=['GET'])
def get_user_data_by_token(token):
	if token != None :
		result = database_helper.get_user_by_token(token)
		if len(result) == 0:
			return 'Profile not found', 404
		else:
			return json.dumps(result), 200
	else:
		return "", 404

'''
@app.route('/changepassword/<token>', methods=['GET'])
def changePassword_data(token):
    if token != None :
        result = database_helper.get_user_by_token(token)
        if len(result) == 0:
            return 'Profile not found', 404
        else:
            return json.dumps(result), 200
    else:
        return "", 404

'''

@app.route('/changepassword/<token>', methods=['POST'])
def changePassword_data(token):
    if token != None :
        result = database_helper.get_user_by_token(token)
        oldPass = request.get_json()["oldPass"]
        newPass = request.get_json()["newPass"]

        

        if len(result) == 0:
            return 'Profile not found', 404
        else:
            return json.dumps(result), 200
    else:
        return "", 404


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
