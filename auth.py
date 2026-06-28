import bcrypt
import database


# ======================================
# PASSWORD FUNCTIONS
# ======================================

def hash_password(password):
    """
    Hash a plain text password.
    """
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, hashed_password):
    """
    Verify a password against its hash.
    """
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )


# ======================================
# REGISTER USER
# ======================================

def register(username, email, password):

    username = username.strip()
    email = email.strip().lower()

    if username == "":
        return False, "Username cannot be empty."

    if email == "":
        return False, "Email cannot be empty."

    if password == "":
        return False, "Password cannot be empty."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if database.get_user(username):
        return False, "Username already exists."

    if database.get_email(email):
        return False, "Email already exists."

    hashed_password = hash_password(password)

    success = database.create_user(
        username,
        email,
        hashed_password
    )

    if success:
        return True, "Account created successfully."

    return False, "Unable to create account."


# ======================================
# LOGIN USER
# ======================================

def login(username, password):

    username = username.strip()

    user = database.get_user(username)

    if user is None:
        return False

    stored_password = user[3]

    return verify_password(
        password,
        stored_password
    )
