from fastapi import APIRouter, HTTPException
from app.data import schemas
from app.data.models import User
from app.utils.auth import create_user, authenticate_user
from app.utils.security import verify_password
from app.routers.user import redis
from app import ACCESS_TOKEN_EXPIRE_MINUTES_REDIS, REDIS_HOST, REDIS_PORT

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create")
async def registration_admin(request: schemas.RequestCreateUser) -> schemas.ResponseUserLogIn:
    user = await create_user(request)
    token = await authenticate_user(data={"sub": request.username})
    
    await redis.set(token, user.username, ex=int(ACCESS_TOKEN_EXPIRE_MINUTES_REDIS))

    return schemas.ResponseUserLogIn(
        user_token=token
    )


@router.post("/log_in")
async def log_in_admin(request: schemas.RequestLogInUser) -> schemas.ResponseUserLogIn:
    user = await User.find_one(User.username == request.username)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect name or password")

    token = await authenticate_user(data={"sub": request.username})
    print(token, user.username, ACCESS_TOKEN_EXPIRE_MINUTES_REDIS)
    await redis.set(token, user.username, ex=int(ACCESS_TOKEN_EXPIRE_MINUTES_REDIS))

    return schemas.ResponseUserLogIn(
        user_token=token
    )
