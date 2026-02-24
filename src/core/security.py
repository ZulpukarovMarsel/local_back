from fastapi.security import HTTPBearer

bearer = HTTPBearer(auto_error=False)
