from fastapi import APIRouter

from config import settings


api_router = APIRouter(prefix=settings.api.prefix)

from .queue import router as rate_router
api_router.include_router(rate_router)