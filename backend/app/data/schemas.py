from __future__ import annotations

from pydantic import BaseModel, Field
from datetime import datetime
from app.data.models import Status, InventoryStatus, Inventory
from typing import List, Optional


class SInventoryId(BaseModel):
    id: str = Field(description="ID инвентаря")


class SInventoryUpdateData(SInventoryId):
    user_id: str = Field(default="ID пользователя")
    name: str = Field(description="Название инвентаря", default="name")
    amount: int = Field(description="Количество инвентаря", default=1)
    state: InventoryStatus | int = Field(description="Состояние инвентаря", default=InventoryStatus.USED)
    description: str = Field(description="Описание инвентаря", default="")


class SInventoryAddData(BaseModel):
    name: str = Field(description="Название инвентаря")
    amount: int = Field(description="Количество инвентаря")
    state: str = Field(description="Состояние инвентаря")
    description: str = Field(description="Описание инвентаря")


class SInventoryAdd(SInventoryAddData):
    updated_at: datetime = Field(description="Дата обновления инвентаря", default=datetime.now())
    created_at: datetime = Field(description="Дата создания инвентаря", default=datetime.now())
    
class SInventoryUpdateImage(SInventoryId):
    user_id: str = Field(default="ID пользователя")
    
class RequestInventoryApplication(BaseModel):
    name: str
    inventory_id: str
    amount: int
    use_purpose: Optional[str] = None

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
    user_id: str
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
    status: int = Field(description="AWAITING = 0, ACCEPTED = 1, CANCELED = 3")

