from datetime import datetime, timezone
from fastapi import Depends, Request
from jose import jwt, JWTError

from app.config import settings
from app.users.dao import UsersDAO
from app.users.models import Users
from app.exceptions import UserIsNotPresentExpception, TokenExpiredException, TokenAbsentException, IncorrectTokenFormat
 
def get_token(request: Request): # request должен вести к эндпоинту ( поэтому у нас много депендсов)
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise IncorrectTokenFormat
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < int(datetime.now(timezone.utc).timestamp())):
        raise TokenExpiredException
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentExpception
    
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotPresentExpception

    return user

# 1 убедиться что токен jwt
# 2 посмотреть что токен действителен (exp eration не прошла)
# 3 параметр sub есть ли (sub - id пользователя)
# 4 если sub = id из бд (только тогда возращается имя пользователя)

