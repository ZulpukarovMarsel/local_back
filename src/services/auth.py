import random
import datetime

from datetime import timezone
from jose import JWTError, jwt
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError

from core.settings import settings
from services import BaseService, UserService
from repositories import UserRepository, OTPRepository
from models import User
from schemas.auth import AuthRegisterSchema, OTPPurpose


OTP_TTL_SECONDS = 300


class AuthService(BaseService):
    def __init__(
            self, user_repo: UserRepository,
            user_service: UserService
    ):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.user_repo = user_repo
        self.user_service = user_service

    def create_token(self, data: dict, expires_delta: int = None, type: str = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_delta)
            to_encode.update({"exp": int(expire.timestamp())})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            return None

    async def get_user_from_token(self, token: str) -> dict:
        payload = self.verify_token(token)
        if payload.get("error"):
            return None
        user_id = payload.get("user_id")
        if not user_id:
            return None
        user = await self.user_repo.get_data_by_id(user_id)
        return user

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.user_repo.get_by_email(email)
        if not user:
            return None
        if not self.user_service.verify_password(password, user.password):
            return None
        return user

    async def register(self, auth_data: AuthRegisterSchema):
        data = auth_data.dict()

        existing = await self.user_repo.get_by_email_and_username(data["email"], data["username"])
        if existing:
            raise HTTPException(status_code=409, detail="User with this email or username already exists")

        data["password"] = self.user_service.hash_password(data["password"])

        try:
            user = await self.user_repo.create_data(data)
            user = await self.user_repo.get_by_id_with_roles(user.id)
            return user
        except IntegrityError:
            raise HTTPException(status_code=409, detail="User with this email already exists")

    async def login(self, email: str, password: str):
        user = await self.authenticate(email, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_payload = {"user_id": user.id, "type": "access"}
        refresh_payload = {"user_id": user.id, "type": "refresh"}

        access_token = self.create_token(access_payload, expires_delta=8640000)
        refresh_token = self.create_token(refresh_payload, expires_delta=8640000)

        if not access_token or not refresh_token:
            raise HTTPException(status_code=500, detail="Token creation failed")
        data = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "email": user.email,
                "full_name": user.full_name()
            }
        return JSONResponse(status_code=201, content=jsonable_encoder(data))

    async def change_password(self, user: User, old_password: str, password: str):
        verify_password = self.user_service.verify_password(old_password, user.password)
        if verify_password:
            user_data = {
                "password": password
            }
            await self.user_service.update_user(user_id=user.id, data=user_data)
            return JSONResponse(status_code=200, content={"message": "Пароль изменен успешно!"})
        raise HTTPException(status_code=400, detail="Старый пароль написан не правильно")


class OTPService(BaseService):
    def __init__(self, user_repo: UserRepository, otp_repo: OTPRepository):
        self.user_repo = user_repo
        self.otp_repo = otp_repo

    @staticmethod
    def _build_message(code: int, purpose: str) -> str:
        title = "OTP code"
        if purpose == OTPPurpose.reset_password.value:
            title = "OTP for password reset"
        elif purpose == OTPPurpose.register.value:
            title = "OTP for registration"

        return f"""
            <!DOCTYPE html>
            <html>
                <body>
                    <p>{title}:</p>
                    <h2 style="font-size: 24px; color: #333; font-weight: bold;">{code}</h2>
                    <p>Copy and paste this code into the app. The code will expire in 5 minutes.</p>
                </body>
            </html>
        """

    @staticmethod
    def _generate_code() -> int:
        code = random.randint(1000, 9999)
        return code

    async def send(self, email: str, purpose: str):
        user = await self.user_repo.get_by_email(email)

        if purpose == "register":
            if user:
                raise HTTPException(status_code=409, detail="User already exists")

        elif purpose == "reset_password":
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

        else:
            raise HTTPException(status_code=400, detail="Unknown OTP purpose")

        await self.otp_repo.delete_by_email_purpose(email, purpose)

        code = self._generate_code()
        message = self._build_message(code, purpose)

        sent = await self.send_message_to_email(
            emails_to=[email],
            message=message
        )

        if not sent:
            raise HTTPException(status_code=500, detail="Send message failed")

        await self.otp_repo.create_data({
            "email": email,
            "code": code,
            "purpose": purpose
        })

        return {"status": "success", "message": f"OTP sent to {email}"}

    async def verify(self, email: str, code: int, purpose: str):
        otp = await self.otp_repo.get_by_email_code_purpose(email, code, purpose)

        if not otp:
            raise HTTPException(status_code=400, detail="Ваш почта или код не правильный")

        now = datetime.datetime.now(timezone.utc)
        diff = now - otp.created_at

        if diff.total_seconds() > OTP_TTL_SECONDS:
            await self.otp_repo.delete_data(otp.id)
            raise HTTPException(status_code=400, detail="Ваш код просрочен, получите новый код")

        await self.otp_repo.delete_data(otp.id)

        return {"status": "success", "message": "OTP verified"}
