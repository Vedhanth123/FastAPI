from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, post, user, vote


load_dotenv()

# ----------------------------------------------- FastAPI starting------------------------------------------
# app = FastAPI(lifespan=lifespan)
app = FastAPI()

origins = ["https://www.google.com"]
# origins = ["*"]  # If public


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # what domains which can talk to our api
    allow_credentials=True,  #
    allow_methods=["*"],  # we can allow only specific methods
    allow_headers=["*"],  # we can allow only specific headers
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def test():
    return "Joker"
