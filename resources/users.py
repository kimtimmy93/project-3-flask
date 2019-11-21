import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, login_required
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

# REGISTER
@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['username'] = payload['username'].lower()
    try:
        models.User.get(models.User.username == payload['username'])
        return jsonify(data={}, status={"code": 401, "message": "username already attached to account"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)
        user_dict = model_to_dict(user)
      
        del user_dict['password']

        return jsonify(data=user_dict, status={"code":201, "message": "Success"})

# LOGIN
@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    try:
        user = models.User.get(models.User.username == payload['username'])
        user_dict = model_to_dict(user)

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
        return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"})
# PROFILE
# @user.route('/user/<username>', methods=["GET"])
# @login_required
# def user(username):
    # user = User.query.filter_by(username=username).first_or_404()
