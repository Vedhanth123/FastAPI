from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from starlette.status import HTTP_404_NOT_FOUND

from app.database import SessionDep
from app.models import (
    CreateUser,
    UserResponse,
    Users,
)
from app.utils import hash_password

# ----------------------------------------------------------------------------------------------
#                                         Users
# ----------------------------------------------------------------------------------------------

router = APIRouter(prefix="/user", tags=["Users"])
# ------------------------------------- Create User ---------------------------------------------


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: CreateUser, session: SessionDep):

    hashed_password = hash_password(user.password.encode("utf-8"))
    user.password = hashed_password
    statement = select(Users).where(Users.email == user.email)
    data = session.exec(statement).first()

    if data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{user.email} already exists!",
        )

    user = Users.model_validate(user)

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# ------------------------------------- Get User ---------------------------------------------
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: SessionDep):

    user = session.get(Users, user_id)

    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"user id {user_id} does not exist"
        )

    return user
