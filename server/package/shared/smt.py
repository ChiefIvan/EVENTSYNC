from flask import url_for, render_template
from flask_mail import Message

from .. import (app, db, mail)
from ..models import Resend


from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature


class Smt:
    def __init__(
        self,
        endpoint="",
        email="",
        name="",
        request=False
    ):
        self.email = email
        self.endpoint = endpoint
        self.name = name
        self.request = request

    def send(self):
        try:
            serializer = URLSafeTimedSerializer(
                app.config["SECRET_KEY"])

            url = url_for(self.endpoint, token=serializer.dumps(
                self.email, salt=app.config["SECURITY_PASSWORD_SALT"]), _external=True)

            token = Resend(
                token=url.split("verified/")[1])

            db.session.add(token)
            db.session.commit()

            template = render_template(
                "smt.html", data={"url": url, "name": self.name})

            msg: Message = Message(
                recipients=[self.email], subject="Verify your Email", html=template)

            mail.send(msg)

            return None, 200

        except BadSignature:
            return {"err": "Sorry, something went wrong, please try again :("}, 400

        except Exception as e:
            print(f"Unexpected error: {e}")

            return {"err": {"timed out": "Email sending timed out. Please try again later.",
                            "connection refused": "Failed to connect to email server. Please try again later."
                            }.get(
                str(e), "There was an error sending the email. Please try again later.")}, 500

    # def request(self):
    #     try:
    #         confirm_url = self.authentication()

    #         reset_token = self.reset(
    #             token=confirm_url.split("confirm_reset/")[1])

    #         self.db.session.add(reset_token)
    #         self.db.session.commit()

    #         template = render_template(
    #             "request_password.html", data=[confirm_url, self.username])

    #         msg: Message = Message(
    #             recipients=[self.data], subject="Request a new Password", html=template)

    #         self.mail.send(msg)

    #     except Exception:
    #         return {"error": self.send_error}
