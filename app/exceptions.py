from fastapi import HTTPException, status

UserALreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User is aldready exists"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not correct email or password"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired"
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is absent"
)

IncorrectTokenFormat = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token format is incorrect"
)

UserIsNotPresentExpception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is not present"
)

RoomCanNotBeBoocked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Room can not be boocked"
)

RoomCanNotBeDeleted = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Room can not be deleted"
)