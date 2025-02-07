from __future__ import annotations

from pydantic import BaseModel, Field
from app.data.models import Status, InventoryStatus, Inventory, User, StatusInventoryRepair
from typing import List, Optional


class SInventoryId(BaseModel):
    _id: str 


class SInventoryUpdateData(SInventoryId):
    id: str = Field(default="ID предмета")
    user_id: str = Field(default="ID пользователя")
    name: str = Field(description="Название инвентаря")
    amount: int = Field(description="Количество инвентаря")
    state: InventoryStatus | int = Field(description="Состояние инвентаря")
    description: str = Field(description="Описание инвентаря")


class SAddInventoryToUser(SInventoryId):
    user_id: str
    inventory_id: str 
    amount: int

class SInventoryAddData(BaseModel):
    name: str = Field(description="Название инвентаря")
    amount: int = Field(description="Количество инвентаря")
    state: InventoryStatus | int = Field(description="Состояние инвентаря")
    description: str = Field(description="Описание инвентаря")


class RequestInventoryApplication(BaseModel):
    inventory_id: str
    amount: int
    use_purpose: Optional[str] = None


class ResponseUserLogIn(BaseModel):
    user_token: str
    
class ResponseAdminLogIn(BaseModel):
    admin_token: str


class RequestCreateUser(BaseModel):
    username: str
    password: str


class ResponseUserAuth(BaseModel):
    username: str


class RequestLogInUser(BaseModel):
    username: str
    password: str


class RequestInventoryRequest(BaseModel):
    user_token: str
    equipment_id: str
    quantity: int
    use_purpose: str


class ResponseInventoryRequest(BaseModel):
    username: str
    Inventory: List[Inventory]
    quantity: int
    use_purpose: str
    status: Status


class ResponseGetInventoryApplication(BaseModel):
    _id: str
    user: User
    inventory: Inventory
    quantity: int
    use_purpose: str
    status: Status


class ResponseInventoryApplication(BaseModel):
    user_id: str
    inventory: Inventory
    quantity: int
    use_purpose: str
    status: Status


class RequestApplicationUpdate(BaseModel):
    application_id: str
    status: int = Field(description="AWAITING = 0, ACCEPTED = 1, CANCELED = 3")
    
class RequestAssignmentInventory(BaseModel):
    user_id: str
    inventory_id: str
    
class CreateInventoryPlan(BaseModel):
    name: str
    manufacturer: str
    price: float
    
class ResponseCreateInventoryPlan(BaseModel):
    _id: str
    name: str
    manufacturer: str
    price: float
    
class UpdateInventoryPlan(BaseModel):
    name: Optional[str] = Field(None)
    manufacturer: Optional[str] = Field(None)
    price: Optional[float] = Field(None)
    
class RequestInventoryRepair(BaseModel):
    inventory_id: str
    description: str
    status: int = Field(description="REPAIR = 0, REPLACING = 1")
    
class ResponseInventoryRepair(BaseModel):
    _id: str
    user: User
    inventory: Inventory
    description: str
    status: int = Field(description="REPAIR = 0, REPLACING = 1")
    
class Statistic(BaseModel):
    inventory_in_use: int
    inventory_repair: int
    need_to_replace: int
    broken: int

class User(BaseModel):
    _id: str
    username: str
    inventory: List[Optional[Inventory]] = []
    
class RequestInventory(BaseModel):
    _id: str
    name: str
    amount: int
    used_by_user: List[str]
    image: Optional[str] = Field(None)
    description: str

    state: InventoryStatus
    updated_at: str
    created_at: str