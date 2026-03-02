import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.algorithms import Algorithm
from jwt.exceptions import InvalidTokenError

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
EXPIRATION_TIME_IN_MINUTES = 30
ALGORITHM = "HS256"


def create_access_token(data: dict):

    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME_IN_MINUTES)
    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
