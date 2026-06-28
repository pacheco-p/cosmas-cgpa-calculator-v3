import bcrypt
import database

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register(username,email,password):
    username=username.strip()
    email=email.strip().lower()
    if not username or not email or not password:
        return False,"All fields are required."
    if database.get_user(username):
        return False,"Username already exists."
    if database.get_email(email):
        return False,"Email already exists."
    database.create_user(username,email,hash_password(password))
    return True,"Account created successfully."

def login(username,password):
    user=database.get_user(username.strip())
    if not user:
        return False
    return verify_password(password,user[3])