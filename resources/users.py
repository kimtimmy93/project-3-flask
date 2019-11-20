import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict
# playhouse is native to peewee

user = Blueprint('users', 'user')

@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['username'] = payload['username'].lower()
    try:
        models.User.get(models.User.username == payload['username'])
        return jsonify(data={}, status={"code": 401, "message": "username already attached to account"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) # bcrypt line for generating the hash
        user = models.User.create(**payload) # put the user in the database

        #login_user
        login_user(user) # starts session

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password
        del user_dict['password'] # delete the password before we return it, because we don't need the client to be aware of it

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    print(payload, ' this is the payload')
    try:
        # Try find the user by their username
        user = models.User.get(models.User.username == payload['username'])
        user_dict = model_to_dict(user) # if you find the User model convert in to a dictionary so you can access it
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            print(user)
            if(payload['username'] == 'admin'):
                user_dict['is_admin'] = True
            return jsonify(data=user_dict, status={"code": 200, "message": "user acquired"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"})

    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"})

# # PROFILE
# @user.route('/user/<username>', methods=["GET"])
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()


