from fastapi import APIRouter, Depends, Response

from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.users.dao import UsersDAO
from app.users.auth import get_password_hash, authentificate_user, create_access_token
from app.exceptions import IncorrectEmailOrPasswordException, UserALreadyExistsException

router = APIRouter(
    prefix="/auth",
    tags=["Auth and Users"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserALreadyExistsException
    
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)

@router.post('/login')
async def login_user(responce: Response, user_data: SUserAuth):
    user = await authentificate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    responce.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token

@router.post("/logout")
async def logout_user(responce: Response):
    responce.delete_cookie("booking_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
