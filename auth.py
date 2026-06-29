import bcrypt
import database

# -----------------------------
# Hash Password
# -----------------------------
def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

# -----------------------------
# Verify Password
# -----------------------------
def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )

# -----------------------------
# Register User
# -----------------------------
def register(username, email, password):
    username = username.strip()
    email = email.strip().lower()

    if database.get_user(username):
        return False, "Username already exists."

    if database.get_email(email):
        return False, "Email already exists."

    hashed_password = hash_password(password)
    database.create_user(username, email, hashed_password)

    return True, "Account created successfully."

# -----------------------------
# Login User
# -----------------------------
def login(username, password):
    user = database.get_user(username)
    if user is None:
        return False

    stored_password = user[3]
    return verify_password(password, stored_password)
