from fastapi import FastAPI

from app.routers import users, auth, groups

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(groups.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
