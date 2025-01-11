from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from app import ALGORITHM, SECURITY_KEY, SECURITY_KEY_USER
from app.data.models import AdminFront, TokenData, User
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import HTTPException

context_pass = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth_bearer = OAuth2PasswordBearer(
    tokenUrl="/api/token/new"
)

def verify_password(plain_password, hashed_password):
    """
    Verify if the provided plain password matches the hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return context_pass.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hash the provided password using bcrypt.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    # print(context_pass.hash(password))
    return context_pass.hash(password)


async def authenticate_user(username: str, password: str):
    """
    Authenticate the user by verifying the username and password.

    Args:
        username (str): The username of the user.
        password (str): The plain text password of the user.

    Returns:
        AdminFront (bool): The user object if authentication is successful, False otherwise.
    """
    #TODO: Handle existans of admin user in Mongo
    user = await AdminFront.find({"username": username}, fetch_links=True).to_list()
    hashed_instance = await user[0].secret.fetch()
    print(hashed_instance.hashed_password)
    if not user:
        return False
    if not verify_password(password, hashed_instance.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.

    Args:
        data (dict): The data to encode in the token.
        expires_delta (timedelta | None): The expiration time delta for the token. Defaults to 15 minutes.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECURITY_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth_bearer)]):
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (Annotated[str, Depends(oauth_bearer)]): The JWT token used for authentication.

    Returns:
        AdminFront: The authenticated user object.

    Raises:
        Errors.CREDENTIALS_EXCEPTION: If the token is invalid, the username is not found in the token,
                                      or the user does not exist in the database.
    """
    try:
        payload = jwt.decode(token, SECURITY_KEY, algorithms=[ALGORITHM])
        print(payload)
        
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=404, detail="Username is not found")
        
        token_data = TokenData(username=username)
    except:
        raise HTTPException(status_code=404, detail="Invalid token")

    user = await AdminFront.find_one(AdminFront.username == token_data.username)
    
    if user is None:
        raise HTTPException(status_code=404, detail="AdminFront User is not found")
    
    return user

async def get_current_user_ordinary(token: str):
    """
    Retrieve the current user based on the provided JWT token.

    Args:
        token (Annotated[str, Depends(oauth_bearer)]): The JWT token used for authentication.

    Returns:
        AdminFront: The authenticated user object.

    Raises:
        Errors.CREDENTIALS_EXCEPTION: If the token is invalid, the username is not found in the token,
                                      or the user does not exist in the database.
    """
    try:
        payload = jwt.decode(token, SECURITY_KEY_USER, algorithms=[ALGORITHM])
        print(payload)
        
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=404, detail="Username is not found")
        
        token_data = TokenData(username=username)
        print(token_data)
    except:
        raise HTTPException(status_code=404, detail="Invalid token")
    
 
    user = await User.find_one(User.email == token_data.username, fetch_links=True)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User is not found")
    
    return user


async def get_current_active_user(
    current_user: Annotated[AdminFront, Depends(get_current_user)],
):
    """
    Retrieve the current active user.

    Args:
        current_user (Annotated[AdminFront, Depends(get_current_user)]): The current authenticated user.

    Returns:
        AdminFront: The current active user object.

    Raises:
        Errors.INACTIVE_USER_EXCEPTION: If the user is inactive.
    """
    
    return current_user