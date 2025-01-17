from fastapi import APIRouter

from app.api.v1.endpoints import user, achievement

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(user.router,
                             prefix="/users",
                             tags=["user"])
api_v1_router.include_router(achievement.router,
                             prefix="/achievements",
                             tags=["achievement"])
