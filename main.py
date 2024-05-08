from fastapi import FastAPI

from app.routers import users, auth#, groups
from app.db.models.base import Base
from app.db.models.comment import Comment
from app.db.models.category import Category
from app.db.models.post import Post
from app.db.models.user import User

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
#app.include_router(groups.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
