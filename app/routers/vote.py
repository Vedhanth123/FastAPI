from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.database import SessionDep
from app.models import CreatePosts, PostResponse, Posts, UpdatePosts, VoteRequest, Votes
from app.oauth2 import get_current_user

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteRequest,
    session: SessionDep,
    current_user: int = Depends(get_current_user),
):

    data = session.exec(
        select(Votes).filter(
            Votes.post_id == vote.post_id and Votes.user_id == current_user.id
        )
    ).first()
    if vote.liked == 1:
        if data:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{current_user.id} has already voted",
            )

        new_data = {"user_id": current_user.id, "post_id": vote.post_id}
        new_data = Votes.model_validate(new_data)
        session.add(new_data)
        session.commit()
        return {"message": "Successfully added vote"}

    elif vote.liked == 0:
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="post with id: not found"
            )

        session.delete(data)
        session.commit()
        return {"message": "Successfully deleted the vote vote"}
