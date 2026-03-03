import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.algorithms import Algorithm
from jwt.exceptions import InvalidTokenError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.database import SessionDep
from app.models import TokenData, Users

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = os.getenv("SECRET_KEY")
EXPIRATION_TIME_IN_MINUTES = 60
ALGORITHM = "HS256"


def create_access_token(data: dict):

    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + timedelta(minutes=EXPIRATION_TIME_IN_MINUTES)
    to_encode.update({"exp": expires})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = id
    except Exception:
        raise credentials_exception

    return token_data


def get_current_user(session: SessionDep, token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate exceptions",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception)
    user = session.get(Users, token)
    return user
