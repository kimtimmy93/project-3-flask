import models
from flask import request, jsnoify, Blueprint
from flask_bcrpyt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('users', 'user')

# REGISTER
@user.route('/register', methods=["POST"])
def register():
    payload = request.get.json()
    payload['username'] = payload['username'].lower()
    try:
        models.User.get(models.User.username == payload['username'])
        return jsonify(data={}, status={'code': 401, 'message': 'email already attached to account'})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        user = models.User.create(**payload)

        login_user(user)
        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))

        del user_dict['password']

        return jsonify(data=user_dict, status={'code':201, 'message': 'Success'})

# LOGIN