from __future__ import annotations

from pydantic import BaseModel, Field
from app.data.models import Status, InventoryStatus, Inventory
from typing import List, Optional


class SInventoryId(BaseModel):
    id: str = Field(description="ID инвентаря")


class SInventoryUpdateData(SInventoryId):
    user_id: str = Field(default="ID пользователя")
    name: str = Field(description="Название инвентаря")
    amount: int = Field(description="Количество инвентаря")
    state: InventoryStatus | int = Field(description="Состояние инвентаря")
    description: str = Field(description="Описание инвентаря")


class SAddInventoryToUser(SInventoryId):
    user_id: str = Field(default="ID пользователя")


class SInventoryAddData(BaseModel):
    name: str = Field(description="Название инвентаря")
    amount: int = Field(description="Количество инвентаря")
    state: InventoryStatus | int = Field(description="Состояние инвентаря")
    description: str = Field(description="Описание инвентаря")


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
