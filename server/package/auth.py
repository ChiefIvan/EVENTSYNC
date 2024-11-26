from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

from . import db, app
from .models import User, Resend
from .shared.smt import Smt
from .shared.validator import validate_entries


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    query = User.query.filter_by(email=data["uname"])
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

    return jsonify({"token": token})


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.json

    is_valid = validate_entries(data)
    if is_valid is not None:
        return jsonify(is_valid), 400

    query = User.query.filter_by(email=data["uname"])
    is_user_exist = query.first()

    if is_user_exist:
        return jsonify(
            {"msg": "Email already exist!, please try another one."}
        ), 400

    smt_check, error_code = Smt(endpoint="auth.email_verification",
                                email=data["uname"], name=data["fname"]).send()

    if isinstance(smt_check, dict):
        return jsonify(smt_check), error_code

    new_user = User(
        email=data["uname"],
        full_name=data["fname"],
        privilege="0",
        institute=data["i_drp"],
        program=data["p_drp"],
        is_confirmed=False,
        psw=generate_password_hash(data["psw"], method="pbkdf2:sha256")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "success"})


@auth.route("/verified/<token>", methods=["GET"])
def email_verification(token):
    try:
        serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
        decoded_data = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=3600)
    except Exception:
        return render_template("message.html",
                               content={
                                   "title": "DOCUTRACKER | Email Verification",
                                   "content": "The confirmation link has expired, or Invalid",
                                   "color": "red"
                               }), 400

    is_token_exist = Resend.query.filter_by(token=token).first()
    if not is_token_exist:
        return render_template("message.html",
                               content={
                                   "title": "DOCUTRACKER | Reset Password",
                                   "content": "You do not have the permission to access this page!",
                                   "color": "red"
                               }), 403

    user = User.query.filter_by(email=decoded_data)
    is_user_exist = user.first()

    if is_user_exist.confirmed:
        return render_template("message.html",
                               content={
                                   "title": "DOCUTRACKER | Email Verification",
                                   "content": "Email Already confirmed!",
                                   "color": "green"
                               })

    is_user_exist.is_confirmed = True
    db.session.commit()

    return render_template("message.html",
                           content={
                               "title": "DOCUTRACKER | Email Verification",
                               "content": "Email confirmed!",
                               "color": "green"
                           })
