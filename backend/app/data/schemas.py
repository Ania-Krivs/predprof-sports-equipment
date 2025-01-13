from pydantic import BaseModel
from app.data.models import Status
    
class ResponseUserLogIn(BaseModel):
    user_token: str
    
class RequestCreateUser(BaseModel):
    username: str
    password: str
    
class ResponseUserAuth(BaseModel):
    username: str
    
class RequestLogInUser(BaseModel):
    username: str
    password: str
    
class RequestEquipmentRequest(BaseModel):
    user_token: str
    equipment_id: str
    quantity: int
    use_purpose: str
    
class ResponseEquipmentRequest(BaseModel):
    username: str
    equipment_id: str
    quantity: int
    use_purpose: str
    status: Status