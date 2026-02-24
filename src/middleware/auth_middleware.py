from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from repositories import UserRepository
from jose import JWTError, jwt
from core.settings import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.user = None
        token = request.headers.get("Authorization")
        if token and token.startswith("Bearer "):
            token = token[7:].strip()

            try:
                payload = jwt.decode(
                    token,
                    settings.JWT_SECRET_KEY,
                    algorithms=[settings.JWT_ALGORITHM],
                )
                user_id = payload.get("user_id")
                token_type = payload.get("type")
                if user_id and token_type == "access":
                    db = request.state.db
                    user_repo = UserRepository(db)
                    user = await user_repo.get_data_by_id(user_id)
                    request.state.user = user

            except JWTError:
                request.state.user = None

        return await call_next(request)
