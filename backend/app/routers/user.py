from fastapi import APIRouter, HTTPException
from app.data import schemas 
from app.data.models import User
from app.utils.auth import create_user, authenticate_user
from app.utils.security import verify_password
from redis import Redis
from app import ACCESS_TOKEN_EXPIRE_MINUTES_REDIS, REDIS_HOST, REDIS_PORT

router = APIRouter(prefix="/user", tags=["User"])

redis = Redis(host=REDIS_HOST, port=REDIS_PORT)

@router.post("/create")
async def registration_user(request: schemas.RequestCreateUser) -> schemas.ResponseUserLogIn:
    user = await create_user(request)
    token = await authenticate_user(data={"sub": request.email})
    
    redis.set(token, user.email, ex=int(ACCESS_TOKEN_EXPIRE_MINUTES_REDIS))

    return schemas.ResponseUserLogIn(
        user_token=token
    )


@router.post("/log_in")
async def log_in_user(request: schemas.RequestLogInUser) -> schemas.ResponseUserLogIn:
    user = await User.find_one(User.email == request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect email or password")
    
    token = await authenticate_user(data={"sub": request.email})
    
    redis.set(token, user.email, ex=int(ACCESS_TOKEN_EXPIRE_MINUTES_REDIS))

    return schemas.ResponseUserLogIn(
        user_token=token
    )