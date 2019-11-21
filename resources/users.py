import models
from flask import request, jsonify, Blueprint, redirect, render_template, url_for
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user,logout_user, login_required
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
      
        del user_dict['password']

        return jsonify(data=user_dict, status={"code":201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    try:
        # Try find the user by their username
        user = models.User.get(models.User.username == payload['username'])
        user_dict = model_to_dict(user) # if you find the User model convert in to a dictionary so you can access it
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            if(payload['username'] == 'admin'):
                user_dict['is_admin'] = True
            return jsonify(data=user_dict, status={"code": 200, "message": "user acquired"})
        else:
            return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"})

# Logout
@user.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify(data={}, status={"code": 200, "message": "Success"})
    
# PROFILE
@user.route('/<username>', methods=["GET"])
@login_required
def profile_page(username):
    try:
        user = models.User.get(models.User.username == username)
        print(user, '<---userrrr')
        return jsonify(data=model_to_dict(user), status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "you must be logged in first"})
