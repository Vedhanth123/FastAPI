

from fastapi import APIRouter

from app.database import SessionDep
from app.models import UserLogin


router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(credentials: UserLogin, session: SessionDep):
    
    