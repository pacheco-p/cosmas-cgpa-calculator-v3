import database


def register(username, email, password):

    if username == "":
        return False, "Username cannot be empty."

    if password == "":
        return False, "Password cannot be empty."

    success = database.create_user(
        username,
        email,
        password
    )

    if success:
        return True, "Account created successfully."

    return False, "Username already exists."


def login(username, password):

    user = database.get_user(username)

    if user is None:
        return False

    # user[3] = password
    if user[3] == password:
        return True

    return False
