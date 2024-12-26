from flask import Blueprint, request, jsonify
from datetime import datetime

from . import db
from .models import Event


views = Blueprint("views", __name__)


@views.route("add_event", methods=["POST"])
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

    return jsonify(data)


@views.route("get_all_event", methods=["GET"])
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
    ])
