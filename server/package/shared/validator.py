from re import compile


def validate_entries(entries):
    excluded_keys = ("institute", "program")

    for key, value in entries.items():
        if len(value) == 0:
            return {"msg": f"Don't leave the {key.capitalize()} input empty!"}

    is_email_format_valid = validate_email_format(entries["uname"])
    if is_email_format_valid is not None:
        return is_email_format_valid

    is_password_string_valid = validate_password(
        entries["psw"], entries["pswcfrm"])
    if is_password_string_valid is not None:
        return is_password_string_valid

    return None


def validate_email_format(email):
    pattern = compile(
        r'^[a-zA-Z0-9._%+-]{5,}@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    if not pattern.match(email):
        return {"msg": "Incorrect Email format!"}

    return None


def validate_password(psw, psw_cnfrm):
    pattern = compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).*$")

    if len(psw) < 8 or len(psw) > 12:
        return {"msg": "Your password must be between 8 and 12 characters long!"}

    if not pattern.match(psw):
        return {"msg": "Your Password must contain atleast 1 Uppercase, 1 Lowercase and a Number!"}

    if psw != psw_cnfrm:
        return {"msg": "Your Password and Password (Confirm) must be the same!"}

    return None
