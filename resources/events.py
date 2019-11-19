import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

event = Blueprint('events', "event")

#post route
@event.route('/', methods=["POST"])
def create_dogs():
    payload = request.get_json()

    event = models.Event.create(**payload)
    print(dir(event))
    
    event_dict = model_to_dict(event)
    return jsonify(data=event_dict, status={'code': 210, "message": "Success"})

#show route

@event.route('/<id>', methods=["GET"])
def get_one_event(id):
    print(id)

    event = models.Event.get_by_id(id)
    print(type(event))
    return jsonify(data=model_to_dict(event), status={"code": 200, "message": "Success"})

