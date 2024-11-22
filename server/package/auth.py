from flask import Blueprint, request, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User
from .shared.smt import Smt
from .shared.validator import validate_entries


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    print(data)

    return jsonify({})


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
