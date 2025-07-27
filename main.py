from fastapi import FastAPI



app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/user/{user_id}")
async def read_user(user_id):
    return {"user_id": user_id, "message": f"User {user_id} details"}


@app.get("/friends/{friend_name}")
async def read_friend(friend_name: Friends):
    return {"friend_name": friend_name, "message": f"Details of {friend_name}"}
