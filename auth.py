import hashlib
import database

# ==========================
# HASH PASSWORD
# ==========================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==========================
# REGISTER USER
# ==========================

def register(username, email, password):

    username = username.strip()
    email = email.strip().lower()

    if username == "":
        return False, "Username cannot be empty."

    if email == "":
        return False, "Email cannot be empty."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if database.get_user(username):
        return False, "Username already exists."

    success = database.create_user(
        username,
        email,
        hash_password(password)
    )

    if success:
        return True, "Account created successfully."

    return False, "Unable to create account."


# ==========================
# LOGIN USER
# ==========================

def login(username, password):

    user = database.get_user(username)

    if user is None:
        return False

    return user["password"] == hash_password(password)


# ==========================
# GET USER
# ==========================

def get_user(username):
    return database.get_user(username)


# ==========================
# UPDATE PROFILE
# ==========================

def update_profile(
    username,
    full_name,
    matric_number,
    department,
    faculty,
    current_level,
    admission_year
):

    database.update_profile(
        username,
        full_name,
        matric_number,
        department,
        faculty,
        current_level,
        admission_year
    )
