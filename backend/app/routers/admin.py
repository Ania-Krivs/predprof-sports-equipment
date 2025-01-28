from fastapi import APIRouter, HTTPException
from app.data import schemas
from app.data.models import User, Admin
from app.utils.auth import create_admin, authenticate_user
from app.utils.security import verify_password
from app.routers.user import redis
from app import ACCESS_TOKEN_EXPIRE_MINUTES_REDIS

router = APIRouter(prefix="/admin", tags=["Admin"])


# @router.post("/create")
# async def registration_admin(request: schemas.RequestCreateUser) -> schemas.ResponseUserLogIn:
#     user = await create_admin(request)
#     token = await authenticate_user(data={"sub": request.username})
    
#     redis.set(token, user.username, ex=int(ACCESS_TOKEN_EXPIRE_MINUTES_REDIS))

#     return schemas.ResponseUserLogIn(
#         user_token=token
#     )


@router.post("/log_in")
async def log_in_admin(request: schemas.RequestLogInUser) -> schemas.ResponseAdminLogIn:
    admin = await Admin.find_one(User.username == request.username)
    if not admin or not verify_password(request.password, admin.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect name or password")

    token = await authenticate_user(data={"sub": request.username})

    redis.set(token, admin.username, ex=int(ACCESS_TOKEN_EXPIRE_MINUTES_REDIS))

    return schemas.ResponseAdminLogIn(
        admin_token=token
    )
