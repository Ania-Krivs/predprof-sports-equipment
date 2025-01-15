from pydantic import BaseModel, Field
from datetime import datetime
from app.data.models import Status, InventoryStatus


class SInventoryId(BaseModel):
    id: str = Field(description="ID инвентаря")


class SInventoryUpdateData(SInventoryId):
    user_id: str = Field(default="ID пользователя")
    name: str = Field(description="Название инвентаря", default="name")
    amount: int = Field(description="Количество инвентаря", default=1)
    state: InventoryStatus | int = Field(description="Состояние инвентаря", default=InventoryStatus.USED)


class SInventoryAddData(BaseModel):
    name: str = Field(description="Название инвентаря", default="name")
    amount: int = Field(description="Количество инвентаря", default=1)
    state: str = Field(description="Состояние инвентаря", default=InventoryStatus.NEW)


class SInventoryAdd(SInventoryAddData):
    updated_at: datetime = Field(description="Дата обновления инвентаря", default=datetime.now())
    created_at: datetime = Field(description="Дата создания инвентаря", default=datetime.now())


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
