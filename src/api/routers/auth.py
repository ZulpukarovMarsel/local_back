import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from jose import JWTError

from repositories import UserRepository
from schemas.auth import (
    AuthLoginSchema, AuthLoginResponseSchema,
    AuthProfileSchema, AuthProfileUpdateSchema,
    AuthRegisterSchema,
    AuthChangePasswordSchema, AuthForgotPasswordSchema, AuthResetPasswordSchema,
    AuthTokenRefreshSchema, AuthTokenRefreshResponseSchema,
    OTPSchema, OTPCheckSchema,
)
from services import UserService, AuthService, OTPService
from dependencies import (
    get_user_repo, get_auth_service, get_user_service,
    get_otp_service, get_profile_update_data, get_current_user
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(lambda: None)]
)


@router.post("/register", response_model=AuthProfileSchema, status_code=201)
async def register(
    auth_data: AuthRegisterSchema,
    auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.register(auth_data)


@router.post("/otp")
async def send_otp(data: OTPSchema, otp_service: OTPService = Depends(get_otp_service)):
    return await otp_service.send(data.email, "register")


@router.post("/otp/check")
async def checking_otp(data: OTPCheckSchema, otp_service: OTPService = Depends(get_otp_service)):
    return await otp_service.verify(data.email, data.code, "register")


@router.post("/login", response_model=AuthLoginResponseSchema)
async def login(auth_data: AuthLoginSchema, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.login(auth_data.email, auth_data.password)


@router.post("/change-password")
async def change_password(
    request: Request,
    auth_data: AuthChangePasswordSchema,
    auth_service: AuthService = Depends(get_auth_service)
):
    user = request.state.user
    return await auth_service.change_password(user, auth_data.old_password, auth_data.password)


@router.post("/forgot-password")
async def forgot_password(data: AuthForgotPasswordSchema, otp_service: OTPService = Depends(get_otp_service)):
    return await otp_service.send(data.email, "reset_password")


@router.post('/reset-password')
async def reset_password(data: AuthResetPasswordSchema, otp_service: OTPService = Depends(get_otp_service), user_service: UserService = Depends(get_user_service), user_repo: UserRepository = Depends(get_user_repo)):
    await otp_service.verify(data.email, data.code, "reset_password")
    user = await user_repo.get_by_email(data.email)
    if not user:
        raise HTTPException(status_code=400, detail="Нету такого пользователья")
    updated = await user_service.update_user(user.id, {"password": data.new_password})
    if not updated:
        raise HTTPException(status_code=500, detail="Не удалось обновить пароль")

    return {"status": "success", "message": "Вы успешно обновили пароль"}


@router.post("/logout")
async def logout(request: Request, response: Response):
    try:
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return JSONResponse(
            status_code=200,
            content={"message": "Вы успешно вышли из системы"}
        )

    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при выходе из системы")


@router.get("/me", response_model=AuthProfileSchema)
async def profile(request: Request, user=Depends(get_current_user)):
    return JSONResponse(status_code=200, content=jsonable_encoder({
        "id": user.id,
        "avatar": f'{str(request.base_url).rstrip("/")}{user.avatar}' if user.avatar else 'none',
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "roles": user.roles,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }))


@router.patch("/me", response_model=AuthProfileSchema)
async def profile_update(
    request: Request, auth_data: AuthProfileUpdateSchema = Depends(get_profile_update_data),
    user_service: UserService = Depends(get_user_service), user=Depends(get_current_user)
):
    return await user_service.update_profile(
        user_id=user.id,
        data=auth_data,
        base_url=str(request.base_url).rstrip("/")
    )


@router.post("/token/refresh", response_model=AuthTokenRefreshResponseSchema)
async def update_access_token(auth_data: AuthTokenRefreshSchema, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.update_access_token(auth_data.refresh_token)
