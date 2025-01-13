from fastapi import HTTPException
from app.utils.security import context_pass
from app.data.models import User
from app.data import schemas
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app import SECURITY_KEY_USER, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

import jwt

context_pass = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(create: schemas.RequestCreateUser):
    
    user_exists = await User.find_one(User.username == create.username)
    if user_exists:
        raise HTTPException(status_code=409, detail="User already exists")
    
    hashed_password = context_pass.hash(create.password)
    user = User(
        username=create.username,
        hashed_password=hashed_password,
        equipment=[]
    )
    
    await user.create()
    return schemas.ResponseUserAuth(
        username=create.username
    )
    
async def authenticate_user(data: dict):
    access_token = await create_token(data)
    
    return access_token


async def create_token(data: dict, expires_delta: timedelta = None):
    '''
        data: email
    '''
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, str(SECURITY_KEY_USER), algorithm=ALGORITHM)
    return encoded_jwt