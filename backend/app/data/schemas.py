from pydantic import BaseModel, EmailStr
    
class ResponseUserLogIn(BaseModel):
    user_token: str
    
class RequestCreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    
class ResponseUserAuth(BaseModel):
    username: str
    email: EmailStr
    
class RequestLogInUser(BaseModel):
    email: EmailStr
    password: str