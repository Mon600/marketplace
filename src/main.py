import uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from api.routers.auth_router import router as auth
from api.routers.user_router import router as user
from api.routers.announcement_router import router as announcement
from api.routers.category_router import router as category
from api.routers.admin_router import router as admin
app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key="secret")
app.include_router(auth)
app.include_router(user)
app.include_router(announcement)
app.include_router(category)

app.include_router(admin)


if __name__ == "__main__":
    uvicorn.run(app)