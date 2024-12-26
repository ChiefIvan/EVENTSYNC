from . import db
from sqlalchemy import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(30))
    privilege = db.Column(db.String(1))
    institute = db.Column(db.String(10))
    program = db.Column(db.String(30))
    is_confirmed = db.Column(db.Boolean, default=False)
    psw = db.Column(db.String(120), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    event_description = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)


class Revoked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(300), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime(timezone=True), nullable=False)


class Resend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(120), nullable=False)
