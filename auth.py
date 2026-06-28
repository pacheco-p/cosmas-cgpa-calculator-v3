import hashlib
import database


# ==========================
# HASH PASSWORD
# ==========================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==========================
# REGISTER
# ==========================

def register(username, email, password):

    if database.get_user(username):
        return False, "Username already exists."

    hashed_password = hash_password(password)

    try:
        database.create_user(
            username,
            email,
            hashed_password
        )

        return True, "Account created successfully."

    except Exception as e:
        return False, str(e)


# ==========================
# LOGIN
# ==========================

def login(username, password):

    user = database.get_user(username)

    if user is None:
        return False

    hashed_password = hash_password(password)

    if user["password"] == hashed_password:
        return True

    return False


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
    level,
    admission_year
):

    database.update_profile(
        username,
        full_name,
        matric_number,
        department,
        faculty,
        level,
        admission_year
    )
