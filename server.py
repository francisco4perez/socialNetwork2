from flask import app, request
from flask import Flask
import database_helper
import json
import random

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

#method that return true if the user with the password and email in parameters exists
@app.route('/signin', methods=['PUT'])
def sign_in():
    # get parameters
    email = request.get_json()['email']
    password = request.get_json()['password']
    # verify that the user exists
    if verify_password(email,password):
        #create a random token
        letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
        token = ""
        for i in range(36) :
            token += letters[int(random.uniform(0,36))]
        # insert token in the database
        result = database_helper.update_token(token,email)
        if result :
			return '{"success": true, "message": "Successfully signed in.", "data":"'+str(token)+'"}', 200
        else :
			return '{"success": false, "message": "Wrong username or password."}', 501
    else:
        return '{"success": false, "message": "Wrong username or password."}', 501

# method that insert a new contact in the dabase if the email is not already used
@app.route('/signup',methods=['PUT'])
def sign_up():
    try:
        # get all parameters
        email = request.get_json()['email']
        password = request.get_json()['password']
        firstname = request.get_json()['firstname']
        familyname = request.get_json()['familyname']
        gender = request.get_json()['gender']
        city = request.get_json()['city']
        country = request.get_json()['country']
		
        # test if the values are not empty and if the password is at least 6 caracters long
        if len(email)!=0 and len(password)>=6 and len(firstname)!=0 and len(familyname)!=0 and len(gender)!=0 and len(city)!=0 and len(country)!=0 :
            exist = database_helper.get_user_by_email(email)
            # if the user doesn't already exist, add the new profile in the database
            if not exist:
                database_helper.insert_user(email,password,"",firstname,familyname,gender,city,country)
                return '{"success": true, "message": "Successfully created a new user."}', 200
            else:
                return '{"success": false, "message": "User already exists."}', 409
        return '{"success": false, "message": "Form data missing or incorrect type."}', 404
    except:
        return '{"success": false, "message": Something went wrong"}',500

#return data of a user given his token
@app.route('/getdatabytoken/<token>', methods=['GET'])
def get_user_data_by_token(token):
	if token != None :
		result = database_helper.get_user_by_token(token)
		if len(result) == 0:
			return '{"success": false, "message": "No such user."}', 404
		else:
			return '{"success": true, "message": "User data retrieved.", "data":"' + json.dumps(result)+'"}', 200
	else:
		return '{"success": false, "message": "You are not signed in."}', 401

#get all the messages of a user given his token
@app.route('/getusermessagesbytoken/<token>',methods=['GET'])
def get_user_messages_by_token(token):
	if token != None :
		result = database_helper.get_user_by_token(token)
		#if this token doesn't exist in the database, return error status
		if not result :
			return '{"success": false, "message": "You are not signed in."}', 401
		return get_user_messages_by_email(token,result[0]['email'])
	else:
		return '{"success": false, "message": "You are not signed in."}', 401

#get all the messages of a profile given his email if the user is signed in
@app.route('/getusermessagesbyemail/<token>/<email>',methods=['GET'])
def get_user_messages_by_email(token,email):
	if email != None :
		exist = database_helper.get_user_by_token(token)
		if exist:
			#search messages in the database with th given email
			result = database_helper.get_messages(email)
			return '{"success": true, "message": "User messages retrieved.", "data":"' + str(result) +'"}',200
		else :
			return '{"success": false, "message": "You are not signed in."}', 401
	else:
		return '{"success": false, "message": "Form data missing or incorrect type."}', 404
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
