from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select
from starlette.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from app.database import SessionDep
from app.models import Token, Users
from app.oauth2 import create_access_token
from app.utils import verify_password

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    session: SessionDep,
    credentials: OAuth2PasswordRequestForm = Depends(),
):

    Statement = select(Users).where(Users.email == credentials.username)
    data = session.exec(Statement).first()

    if not data:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"User with email {credentials.email} not found",
        )

    if verify_password(
        credentials.password.encode("utf-8"), data.password.encode("utf-8")
    ):
        access_token = create_access_token({"user_id": data.id})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"Invalid credentials for {credentials.email}",
        )
