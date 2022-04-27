from flask import request, json, jsonify
from src.models import Contract, User
from src.utils import hashing, get_text_from_boolean
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
        'sms': get_text_from_boolean(user.receive_sms),
        'whatsapp': get_text_from_boolean(user.receive_whatsapp),
        'call': get_text_from_boolean(user.receive_call),
        'email': get_text_from_boolean(user.receive_email)
    })

    return response

@app.route("/user/history/<string:user_email>", methods=['GET'])
def get_user_history_by_email(user_email):
    user = User.find_by_email(db, user_email)

    response = jsonify({
        'history': user.history
    })

    return response