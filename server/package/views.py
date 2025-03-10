from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from sqlalchemy.orm import joinedload
from datetime import datetime
from base64 import b64decode,b64encode
from uuid import uuid4
from io import BytesIO
from PIL import Image
from os import path
from barcode import EAN13
from barcode.writer import ImageWriter


from . import db, app
from .models import Event, User, Revoked, user_event


views = Blueprint("views", __name__)


def handle_file(name):
    _dir = f"{app.static_folder}\\img\\user\\{name}.webp"

    if path.exists(_dir):
        with open(f"{_dir}", "rb") as file:
            img = file.read()

        return b64encode(img).decode('utf-8')
    
    return None

def create_barcode(code):
    data = EAN13(code, writer=ImageWriter())
    io = BytesIO()
    data.write(io)
    return b64encode(io.getvalue()).decode('utf-8')


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

    code = user.code
    return jsonify({
        "img":  handle_file(user.img),
        "email": user.email,
        "full_name": user.full_name,
        "privilege": user.privilege,
        "s_id": user.s_id,
        "institute": user.institute,
        "program": user.program,
        "code": code,
        "barcode": create_barcode(code),
    }), 200
    

@views.route("/get_all_reg_users", methods=["POST"])
@jwt_required()
def get_all_reg_users():
    data = request.json
    registered_users = db.session.query(User).join(User.registered_events).filter(Event.id == data["event_id"]).all()
    return jsonify([{
        "full_name": user.full_name,
    } for user in registered_users])


@views.route("/get_all_users", methods=["GET"])
@jwt_required()
def get_all_users():
    users = User.query.all()

    return jsonify([{
        "img": handle_file(user.img),
        "full_name": user.full_name,
        "s_id": user.s_id,
        "institute": user.institute,
        "program": user.program,
        "privilege": "User",
        "code": user.code,
        "barcode": create_barcode(user.code)
    } for user in users if user.full_name != "Admin"])


@views.route("/delete_event", methods=["POST"])
@jwt_required()
def get_all_users():
    data = request.json

    event = Event.user.query.filter_by(data["id"])

    if event:
        db.session.delete(event)
        db.session.commit()


@views.route("/upl_prf", methods=["POST"])
@jwt_required()
def upload_prf():
    data = request.json
    current_user = get_jwt_identity()

    user = User.query.filter_by(id=current_user).first()

    decoded_bytes = b64decode(data["img"])
    image_file = BytesIO(decoded_bytes)

    img = Image.open(image_file)
    img = img.convert('RGB')

    filename = str(uuid4()) if not user.img else user.img

    if filename != user.img:
        user.img = filename
        db.session.commit()

    img.save(f"{app.static_folder}\\img\\user\\{filename}.webp")


    return jsonify({})


@views.route("/add_event", methods=["POST"])
@jwt_required()
def add_event():
    data = request.json

    try:
        new_event = Event(
            event_name=data["event_name"],
            event_description=data["event_description"],
            date=datetime.strptime(data["event_date"], "%B %d, %Y"),
            start_time=data["event_start_time"],
            end_time=data["event_end_time"]
        )

        db.session.add(new_event)
        db.session.commit()

    except Exception as e:
        db.session.rollback()

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

@views.route("/register_user", methods=["POST"])
@jwt_required()
def register_user_to_event():
    data = request.json

    print(data["code"][:-1])

    if not data.get('code'):
        return jsonify({'msg': 'Missing required fields'}), 400

    try:
        user = User.query.filter_by(code=data["code"][:-1]).first()

        if not user:
            return jsonify({'msg': 'No User Associates with the bar code!'}), 404

        registration = db.session.query(user_event).filter(
                user_event.user_id == user.id,
                user_event.event_id == data["id"]
            ).first()

        if registration:
            return jsonify({
                "msg": "User's Attendance for this event already marked!"
            }), 400

        association = user_event(user_id=user.id, event_id=data["id"])
        
        db.session.add(association)

        try:
            db.session.commit()
            return jsonify({
                "msg": "User's Attendance for this event marked successfully!"
            }), 200
        
        except Exception as e:
            db.session.rollback()
            print(f"Error committing transaction: {str(e)}")

            return jsonify({
                "msg": "Error, Try Again!"
            }), 500
        
    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error: {str(e)}")
        
        return jsonify({
            "msg": "An unexpected error occurred"
        }), 500
    

@views.route("/generate_pdf", methods=["POST"])
@jwt_required()
def generate_pdf():
    data = request.json
    event = Event.query.filter_by(id=data["id"]).first()
    registered_users = (
      db.session.query(User)
      .join(User.registered_events)
      .filter(Event.id == data["id"])
      .all()
    )

    if len(registered_users) == 0:
        return jsonify({"msg": "No registered students yet!"}), 404

    pdf_file_name = f"{event.event_name}.pdf"
    pdf = canvas.Canvas(pdf_file_name, pagesize=letter)
    pdf.setTitle("Present Students")

    pdf.setFont("Courier", 12)

    pdf.drawCentredString(300, 770, "Present Students")

    table_data = [["Student Name", "Student ID", "Status"]]
    for user in registered_users:
        table_data.append([user.full_name, user.s_id, "Present"])

    table = Table(table_data)
    style = TableStyle([
      ("FONTNAME", (0, 0), (-1, -1), "Courier"),
      ("FONTSIZE", (0, 0), (-1, -1), 12),
      ("ALIGN", (1, 0), (-1, -1), "CENTER"),
      ("ALIGN", (0, 0), (0, -1), "LEFT"),
      ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
    ])
    table.setStyle(style)

    table.wrapOn(pdf, 50, 600)
    table.drawOn(pdf, 50, 600)

    pdf.save()

    with open(pdf_file_name, "rb") as pdf_file:
        base64_pdf = b64encode(pdf_file.read()).decode("utf-8")

    return jsonify({"pdf_base64": base64_pdf, "filename": pdf_file_name})

    
@views.route("/logout", methods=["GET"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now()
    revoked_token = Revoked(jti=jti, revoked_at=now)
    db.session.add(revoked_token)
    db.session.commit()
    return jsonify({}), 200