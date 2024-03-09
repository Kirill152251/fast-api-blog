from fastapi import FastAPI

from app.routers import users
from app.db.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
