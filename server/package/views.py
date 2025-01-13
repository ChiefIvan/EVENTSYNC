from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime

from . import db
from .models import Event, User, Revoked


views = Blueprint("views", __name__)

@views.route("/get_privilege", methods=["GET"])
@jwt_required()
def get_user_privilege():
    current_user = get_jwt_identity()

    query = User.query.filter_by(id=current_user)
    user = query.first()
    
    return jsonify({
        "privilege": user.privilege
    }), 200

@views.route("/get_user_info", methods=["GET"])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    query = User.query.filter_by(id=current_user)
    user = query.first()

    return jsonify({
        "email": user.email,
        "full_name": user.full_name,
        "privilege": user.privilege,
        "institute": user.institute,
        "program": user.program,
        "code": user.code,
    }), 200
    
    


@views.route("/add_event", methods=["POST"])
@jwt_required()
def add_event():
    data = request.json

    new_event = Event(
        event_name=data["event_name"],
        event_description=data["event_description"],
        date=datetime.strptime(data["event_date"], "%B %d, %Y"),
        start_time=data["event_start_time"],
        end_time=data["event_end_time"]
    )

    db.session.add(new_event)
    db.session.commit()

    return jsonify(data), 200


@views.route("/get_all_event", methods=["GET"])
@jwt_required()
def get_all_event():
    events = Event.query.all()

    return jsonify([
        {
            "id": event.id,
            "event_name": event.event_name,
            "event_description": event.event_description,
            "event_date": event.date.strftime("%B %d, %Y"),
            "event_start_time": event.start_time,
            "event_end_time": event.end_time,
        } for event in events
    ]), 200
    
@views.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now()
    revoked_token = Revoked(jti=jti, revoked_at=now)
    db.session.add(revoked_token)
    db.session.commit()
    return jsonify({}), 200