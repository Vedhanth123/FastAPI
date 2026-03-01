import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password, bcrypt.gensalt())