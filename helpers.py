from functools import wraps

def strong_password(s):
    specials = [
        "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "[", "]", "{", "}", "?"
    ]
    special = 0
    number = 0
    alphabet = 0
    for i in s:
        if i in specials:
            special += 1
        if i.isnumeric():
            number += 1
        if i.isalpha():
            alphabet += 1

    if special >= 1 and number >= 1 and alphabet >= 1 and len(s) >= 6:
        return True
    else:
        return False


def login_required(f):
    """ Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function