from fastapi import APIRouter

from api.routers.users import router as user_router
from api.routers.auth import router as auth_router
# from api.routers.roles import router as role_router
# from api.routers.projects import router as project_router


router = APIRouter(prefix="/api")
router_list = [
    auth_router,
    user_router,
    # role_router,
    # project_router,
]

for r in router_list:
    router.include_router(r)

__all__ = [
    "router",
]
