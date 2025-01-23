from . import db
from sqlalchemy.orm import relationship


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(30))
    privilege = db.Column(db.String(1))
    institute = db.Column(db.String(10))
    program = db.Column(db.String(30))
    code = db.Column(db.String(50))
    is_confirmed = db.Column(db.Boolean, default=False)
    psw = db.Column(db.String(120), nullable=False)
    otp_access = db.relationship("Otp")
    registered_events = relationship("Event", secondary="user_event", back_populates="registered_users")


class Otp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pin = db.Column(db.String(10))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(50), nullable=False)
    event_description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)
    registered_users = relationship("User", secondary="user_event", back_populates="registered_events")


class Revoked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(300), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime(timezone=True), nullable=False)


user_event = db.Table('user_event',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)


# Get all users registered to a specific event
# registered_users = db.session.query(User).join(user_event, User.id == user_event.user_id).filter(user_event.event_id == event_id).all()

# Get all events registered by a specific user
# registered_events = db.session.query(Event).join(user_event, Event.id == user_event.event_id).filter(user_event.user_id == user_id).all()
