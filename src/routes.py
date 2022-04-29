from flask import request, json, jsonify
from src.models import Contract, User, Notification
from src.utils import get_text_from_boolean
from src import app, db

@app.route('/contract', methods=['POST'])
def create_contract():
    req = request.json # getting body from request
    contract = Contract(req) # create object
    contract.save(db) # save on database
    # create json response
    response = jsonify({
        'contract': contract.asdict()
    })

    return response
@app.route('/contract/latest', methods=['GET'])
def get_latest_contract():
    contract = Contract.get_latest(db) # getting latest from db
    # create json response
    response = jsonify({
        'contract': contract.asdict()
    })
    return response

@app.route("/user", methods=['POST'])
def create_user():
    req = request.json # getting body from request
    user = User(req) # create object
    user.save(db) # save on database
     # create json response
    response = jsonify({
        'receipt': user.create_setting_message(),
        'user': user.asdict()
    })

    return response

@app.route("/user/<string:user_email>", methods=['GET'])
def get_user_by_email(user_email):
    user = User.find_by_email(db, user_email)

    response = jsonify({
        'user': user.asdict()
    })

    return response


@app.route("/user/notification/<string:user_email>", methods=['GET'])
def get_user_notifications_by_email(user_email):
    user = User.find_by_email(db, user_email)

    response = jsonify({
        'notification': user.notification
    })

    return response

@app.route("/user/history/<string:user_email>", methods=['GET'])
def get_user_history_by_email(user_email):
    user = User.find_by_email(db, user_email)

    response = jsonify({
        'history': user.history
    })

    return response

@app.route("/user/notification/<string:user_email>", methods=['PUT'])
def update_user_notification(user_email):
    req = request.json
    notification = Notification(req)

    User.update_notifications(user_email, db, notification)

    user = User.find_by_email(db, user_email)

    response = jsonify({
        'notification': user.notification,
        'receipt': user.create_setting_message(),
        'key': notification.hashed_key
    })

    return response

@app.route("/user/contract/<string:user_email>", methods=['PUT'])
def update_user_contract(user_email):
    req = request.json
    User.update_contract(user_email, db, req['contract'])
    user = User.find_by_email(db, user_email)

    response = jsonify({
        'receipt': user.create_contract_message(),
        'contract': user.contract
    })

    return response


@app.route("/user/contract/<string:user_email>", methods=['GET'])
def get_user_contract(user_email):
    user = User.find_by_email(db, user_email)

    response = jsonify({
        'contract': user.contract
    })

    return response 
