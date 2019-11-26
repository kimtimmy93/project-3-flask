import models
from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

userEvent = Blueprint('userEvents', 'userEvent')

#HOME ROUTE
# @userEvent.route('/', methods=["GET"])
# def get_all_userEvents():
#     try:
#         userEvents = [model_to_dict(userEvent) for userEvent in
#         models.UserEvent.select()]
#         return jsonify(data={}, status={"code": 200, "message": "Error getting the resources"})
#     except models.DoesNotExist:
#         return jsonify(data={}, status={"code": 401,
#         "message": "Error getting the resources"})

   
   
    #POST ROUTE
@userEvent.route('/', methods=["POST"])
def create_userEvents():
    payload = request.get_json()
    userEvent = models.UserEvent.create(**payload)
    print(model_to_dict(userEvent)['event'])

    userEventList = models.UserEvent.select().where(models.UserEvent.user == userEvent.id)
    print(model_to_dict(userEventList))

    # for event in userEventList:
    #     event_dict = model_to_dict(event)
    #     print(event_dict)
    return jsonify(data={}, status={"code": 201, "message": "success"})
    # userEvent = models.UserEvent.create(**payload)
    # userEvent_dict = model_to_dict(userEvent)
    # return jsonify(data=userEvent_dict, status={"code":
    # 201, " m 
    #   essage": "Success"})