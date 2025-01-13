from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from random import choices

from . import db, app
from .models import User, Otp
from .shared.smt import Smt
from .shared.validator import validate_entries


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    query = User.query.filter_by(email=data["email"])
    is_user_exist = query.first()

    if not is_user_exist:
        return jsonify(
            {"msg": "Account doesn't exist!"}
        ), 404

    if not check_password_hash(is_user_exist.psw, data["psw"]):
        return jsonify(
            {"msg": "Incorrect Password, please try again!"}
        ), 401

    if not is_user_exist.is_confirmed:
        return jsonify(
            {"msg": "Please verify your account first!"}
        ), 400

    token = create_access_token(identity=is_user_exist)

    return jsonify({"token": token, "privilege": is_user_exist.privilege})


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json

    is_valid = validate_entries(data)
    if is_valid is not None:
        return jsonify(is_valid), 400

    query = User.query.filter_by(email=data["email"])
    is_user_exist = query.first()

    if is_user_exist:
        return jsonify(
            {"msg": "Email already exist!, please try another one."}
        ), 400

    new_user = User(
        email=data["email"],
        full_name=data["fname"],
        privilege="0",
        institute=data["i_drp"],
        program=data["p_drp"],
        code=str(choices(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], k=12)),
        is_confirmed=False, 
        psw=generate_password_hash(data["psw"], method="pbkdf2:sha256")
    )

    db.session.add(new_user)
    db.session.commit()

    pin = choices(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], k=6)

    smt_check, error_code = Smt(
        email=data["email"], 
        name=data["fname"],
        pin="".join(pin)).send()

    if isinstance(smt_check, dict):
        return jsonify(smt_check), error_code

    user = User.query.filter_by(email=data["email"]).first()
    new_pin = Otp(pin="".join(pin), user_id=user.id)

    db.session.add(new_pin)
    db.session.commit()

    return jsonify({"msg": "success"})


@auth.route("/request_otp", methods=["POST"])
def otp():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()
    is_otp_exist = Otp.query.filter_by(user_id=user.id).first()

    if not is_otp_exist:
        return jsonify(
            {"msg": "Incorrect pin!."}
        ), 400

    user.is_confirmed = True
    db.session.commit()

    token = create_access_token(identity=user)

    return jsonify({
        "token": token 
    })

    