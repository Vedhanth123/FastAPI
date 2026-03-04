from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers import auth, post, user, vote

from app.database import lifespan

load_dotenv()

# ----------------------------------------------- FastAPI starting------------------------------------------
app = FastAPI(lifespan=lifespan)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
