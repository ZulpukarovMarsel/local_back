from fastapi import APIRouter

from api.routers.users import router as user_router
from api.routers.auth import router as auth_router
from api.routers.post import router as post_router
from api.routers.comment import router as comment_router
from api.routers.like import router as like_router
from api.routers.favorite import router as favorite_router


router = APIRouter(prefix="/api")
router_list = [
    auth_router,
    user_router,
    post_router,
    comment_router,
    like_router,
    favorite_router

]

for r in router_list:
    router.include_router(r)

__all__ = [
    "router",
]
