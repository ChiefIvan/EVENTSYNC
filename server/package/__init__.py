from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from os import getenv
from dotenv import load_dotenv
from datetime import timedelta
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()

app.config["SECRET_KEY"] = getenv("SK")
app.config["JWT_SECRET_KEY"] = getenv("SK")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["SECURITY_PASSWORD_SALT"] = getenv("SALT")
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{getenv('DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_DEFAULT_SENDER"] = getenv("EMAIL")
app.config["MAIL_USERNAME"] = getenv("EMAIL")
app.config["MAIL_PASSWORD"] = getenv("PASS")

db.init_app(app)
jwt.init_app(app)
mail.init_app(app)

from .auth import auth
from .views import views

from .models import (
    User, Revoked
)


app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(views, url_prefix="/views")


def tables_exist():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    required_tables = ["user", "revoked"]
    return all(table in tables for table in required_tables)


def create_admin():
    add_admin = User(
        email=getenv("ADMIN_EMAIL"),
        full_name="Admin",
        privilege="1",
        institute=None,
        program=None,
        is_confirmed=True,
        psw=generate_password_hash(
            getenv("ADMIN_PASS"), method="pbkdf2:sha256")
    )

    db.session.add(add_admin)
    db.session.commit()


with app.app_context():
    if not tables_exist():
        db.create_all()
        create_admin()


@jwt.user_identity_loader
def user_loader(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, decoded_token):
    id = decoded_token["sub"]
    return User.query.get(int(id))


@jwt.token_in_blocklist_loader
def revoked_tokens(jwt_header, decoded_token):
    jti = decoded_token['jti']
    revoked_token = Revoked.query.filter_by(jti=jti).scalar()
    return revoked_token is not None


def server():
    return app
