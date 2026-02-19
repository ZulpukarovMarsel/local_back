from fastapi import APIRouter, Depends, HTTPException, Request, Response


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(lambda: None)]
)


@router.post("/post", response_model=AuthProfileSchema)
async def get_posts(request: Request, auth_data: AuthRegisterSchema):
    db = request.state.db
    user_repo = UserRepository(db)
    user_service = UserService(user_repo)
    user_data = auth_data.dict()
    existing = await user_repo.get_user_by_email(user_data['email'])
    if existing:
        raise HTTPException(status_code=409, detail="User with this email already exists")
    new_user = await user_service.create_user(user_data)
    return new_user

