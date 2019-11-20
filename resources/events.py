import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict


event = Blueprint('events', 'event')

# Home
@event.route('/', methods=["GET"])
def get_all_events():
    try: 
        events = [model_to_dict(event) for event in models.Event.select()]

        print(events)
        return jsonify(data=events, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message":"Error getting the resource"})

# POST
@event.route('/', methods=["POST"])
def create_events():
    payload = request.get_json()
    print(payload, 'payload')

    event = models.Event.create(**payload)

    print(dir(event))

    print(model_to_dict(event))
    event_dict = model_to_dict(event)
    return jsonify(data=event_dict, status={"code": 201, "message": "Success"})

# Show
@event.route('/<id>', methods=["GET"])
def get_one_event(id):
    print(id)
    event = models.Event.get_by_id(id)

    return jsonify(data=model_to_dict(event), status={"code": 200, "message": 'Success'})

# Update
@event.route('/<id>', methods=["PUT"])
def update_event(id):
    payload = request.get_json()

    query = models.Event.update(**payload).where(models.Event.id == id)

    event = models.Event.get_by_id(id)

    event_dict = model_to_dict(event)

    return jsonify(data=event_dict, status={"code": 200, "message": "resource updated successfully"})

#Update, Edit, Delete for admin only