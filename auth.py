import hashlib
import database


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def signup(username, email, password):

    password = hash_password(password)

    return database.create_user(
        username,
        email,
        password
    )


def login(username, password):

    user = database.get_user(username)

    if not user:
        return False

    if user["password"] == hash_password(password):
        return True

    return False


def get_user(username):
    return database.get_user(username)
