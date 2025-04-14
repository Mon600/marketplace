import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api.routers.auth_router import router as auth
from api.routers.user_router import router as user
from api.routers.annoncement_router import router as announcement
from api.routers.file_router import router as file

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="secret")
app.include_router(auth)
app.include_router(user)
app.include_router(announcement)
app.include_router(file)

if __name__ == "__main__":
    uvicorn.run(app)