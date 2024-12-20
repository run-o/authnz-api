from fastapi import APIRouter

from app.api.routes import users
from app.api.routes import auth
from app.api.routes import user_data


api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(user_data.router)