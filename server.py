from gevent.wsgi import WSGIServer
from flask import app, request
from flask import Flask
import database_helper
import json
import random

app = Flask(__name__)
app.debug = True


#Connect database before request
@app.before_request
def before_request():
    database_helper.connect_db()

#Close database after request
@app.teardown_request
def teardown_request(exception):
    database_helper.close_db()


@app.route('/')
def main():
    return app.send_static_file('client.html')

#return true if the email and password in parameter correspond to a profile in the database
def verify_password(email, password):
    result = database_helper.get_user_by_email_and_password(email,password)
    try :
        if result and len(password)>=6:
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
        if len(email)!=0 and len(password) >= 6 and len(firstname)!=0 and len(familyname)!=0 and len(gender)!=0 and len(city)!=0 and len(country)!=0 :
            exist = database_helper.get_user_by_email(email)
            # if the user doesn't already exist, add the new profile in the database
            if not exist:
                database_helper.insert_user(email,password,"",firstname,familyname,gender,city,country)
                return '{"success": true, "message": "Successfully created a new user."}', 200
            else:
                return '{"success": false, "message": "User already exists."}', 409
        return '{"success": false, "message": "Form data missing or incorrect type."}', 404
    except:
        return '{"success": false, "message": "Something went wrong"}',500

#method that delete the current session and the token
@app.route('/signout',methods=['PUT'])
def sign_out():
    token = request.get_json()['token']
    result = database_helper.get_user_by_token(token)

    if len(result) == 0:
        return '{"success": false, "message": "No such token"}',400

    if token != None:
        if database_helper.delete_token(token):
            return '{"success": true, "message": "Signout Successfull!."}', 200
        else:
            return '{"success": false, "message": "Something went wrong"}',500
    else:
        return '{"success": false, "message": "No token found"}',500


#get data of a user given his token
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

#get data of a user given his email
@app.route('/getdatabyemail/<token>/<email>', methods=['GET'])
def get_user_data_by_email(token,email):
    if email != None :
        #checks if the token exist in the database
        exist = database_helper.get_user_by_token(token)
        if exist:
            #search data in the database with the given email
            result = database_helper.get_user_by_email(email)
            if len(result) == 0:
                return '{"success": false, "message": "No such user."}', 404
            else:
                return '{"success": true, "message": "User data retrieved.", "data":"' + str(result) +'"}',200
        else :
            return '{"success": false, "message": "You are not signed in."}', 401
    else:
        return '{"success": false, "message": "Form data missing or incorrect type."}', 404


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

#post a message on a profile with the email of the writer and his message
@app.route('/postmessage',methods=["POST"])
def post_message():
    try:
        # get all parameters
        token = request.get_json()['token']
        message = request.get_json()['message']
        email = request.get_json()['email']
        existtoken = database_helper.get_user_by_token(token)
        existemail = database_helper.get_user_by_email(email)
        if existtoken:
            if existemail :
                #get the name of the writer
                writer = existtoken[0]['email']
                result = database_helper.insert_message(email,writer,message)
                if result :
                    return '{"success": true, "message": "the message has been posted"}', 200
                else :
                    return '{"success": false, "message": "A problem has occured in the database"}', 500
            else :
                return '{"success": false, "message": "this email does not exist"}', 401
        else :
            return '{"success": false, "message": "You are not signed in."}', 401
    except:
        return '{"success": false, "message": "Something went wrong"}',500

#Function to change password by given token
@app.route('/changepassword/<token>', methods=['POST'])
def changePassword_data(token):
    if token != None :
        result = database_helper.get_user_by_token(token)

        #verify if there is token
        if len(result) != 0:
            user = result[0]
        else:
            return "There is no user with such token!", 200

        #json inputs
        oldPass = request.get_json()["oldpass"]
        newPass = request.get_json()["newpass"]
        
        #to verify if the oldpassword is right and has more lenght than six letters
        if verify_password(user["email"],oldPass):
            if len(oldPass) >= 6:
                #if changing is succesfull
                if database_helper.update_password(token,oldPass,newPass):
                    return '{"success": true, "message": "Password changed"}',200
                else:
                    return '{"success": false, "message": "Updating went wrong!"}',500
            else:
                return '{"success": false, "message": "Password is too short!"}',500

        else:
            return '{"success": false, "message": "Wrong old password!"}',500
    else:
        return "", 404


if __name__ == '__main__':

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
