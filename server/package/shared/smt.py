from flask import render_template
from flask_mail import Message

from .. import  mail


class Smt:
    def __init__(
        self,
        email="",
        name="",
        pin="",
    ):
        self.email = email
        self.name = name
        self.pin = pin

    def send(self):

        template = render_template(
            "smt.html", data={"pin": self.pin, "name": self.name})

        msg: Message = Message(
            recipients=[self.email], subject="Verify your Email", html=template)

        mail.send(msg)

        return None, 200
