import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.algorithms import Algorithm
from jwt.exceptions import InvalidTokenError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.models import TokenData

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = os.getenv("SECRET_KEY")
EXPIRATION_TIME_IN_MINUTES = 30
ALGORITHM = "HS256"


def create_access_token(data: dict):

    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME_IN_MINUTES)
    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    print("hello verify")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")
        print(id)
        if not id:
            raise credentials_exception
        token_data = id
    except Exception:
        raise credentials_exception

    print(token_data)
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):

    print("hello")
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate exceptions",
        headers={"WWW-Authenticate": "Bearer"},
    )

    print("hello")
    return verify_access_token(token, credentials_exception)
