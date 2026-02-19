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
from services import BaseService, UserService, AuthService, OTPService
from dependencies import get_user_repo, get_auth_service, get_user_service, get_otp_service

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


@router.get("/me", response_model=AuthProfileSchema)
async def profile(request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="User is not authanticate")
    data = {
        "id": user.id,
        "image": f'{str(request.base_url).rstrip("/")}{user.image}' if user.image else 'none',
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "roles": user.roles,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    return JSONResponse(status_code=200, content=jsonable_encoder(data))


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


@router.patch("/me", response_model=AuthProfileSchema)
async def profile_update(request: Request, auth_data: AuthProfileUpdateSchema = Depends()):
    try:
        db = request.state.db
        user = request.state.user
        if not user:
            raise HTTPException(status_code=401, detail="User is not authenticated")
        update_data = auth_data.dict(exclude_unset=True)
        if "image" in update_data:
            update_data.pop("image")

        if auth_data.image:
            image_info = await BaseService.upload_image(auth_data.image, "avatars")
            update_data["image"] = image_info['image_path']
            {str(request.base_url).rstrip("/")}

        user_repo = UserRepository(db)
        profile_updated = await user_repo.patch_user(user.id, update_data)
        if profile_updated.image:
            profile_updated.image = f'{str(request.base_url).rstrip("/")}{profile_updated.image}'
        return AuthProfileSchema.model_validate(profile_updated)

    except Exception as e:
        logger.exception("Ошибка в обновлении профиля")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/token/refresh", response_model=AuthTokenRefreshResponseSchema)
async def update_access_token(request: Request, auth_data: AuthTokenRefreshSchema):
    user = request.state.user
    auth_data = auth_data.dict()
    try:
        verify_token = AuthService().verify_token(auth_data['refresh_token'])
        if verify_token:
            access_payload = {"user_id": user.id, "type": "access"}

            access_token = AuthService().create_token(access_payload, expires_delta=8640000)
            data = {
                "access_token": access_token,
                "token_type": "access"
            }
            return JSONResponse(status_code=200, content=jsonable_encoder(data))
    except JWTError as e:
        raise HTTPException(status_code=401, detail=e)
