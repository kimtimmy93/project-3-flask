import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

event = Blueprint('events', 'event')

#HOME ROUTE
@event.route('/', methods=["GET"])
def get_all_events():
    try:
        events = [model_to_dict(event) for event in models.Event.select()]
        return jsonify(data=events, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#POST ROUTE
@event.route('/', methods=["POST"]) 
def create_events():
    payload = request.get_json()
    event = models.Event.create(**payload)
    event_dict = model_to_dict(event)
    return jsonify(data=event_dict, status={"code": 201, "message": "Success"})

#SHOW ROUTE
@event.route('/<id>', methods=["GET"])
def get_one_event(id):
    event = models.Event.get_by_id(id)
    return jsonify(data=model_to_dict(event), status={"code": 200, "message": 'Success'})

#UPDATE ROUTE
@event.route('/<id>', methods=["PUT"])
def update_event(id):
    payload = request.get_json()
    query = models.Event.update(**payload).where(models.Event.id == id)
    query.execute()
    event = models.Event.get_by_id(id)
    event_dict = model_to_dict(event)
    return jsonify(data=event_dict, status={"code": 200, "message": "resource updated successfully"})

#DELETE ROUTE
@event.route('/<id>', methods=["DELETE"])
def delete_event(id):
    query = models.Event.delete().where(models.Event.id==id)
    query.execute()
    return jsonify(data='resource successfully deleted', status={"code": 200, "message": "resource deleted successfully"})

