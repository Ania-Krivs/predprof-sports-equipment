from beanie import Document, Link
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import IntEnum


class Status(IntEnum):
    AWAITING = 0
    ACCEPTED = 1
    CANCELED = 2
    RETURNED = 3


class InventoryStatus(IntEnum):
    BROKEN = 0
    USED = 1
    NEW = 2
    
class StatusInventoryRepair(IntEnum):
    REPAIR = 0
    REPLACING = 1


class Inventory(Document):
    name: str
    amount: int
    used_by_user: List[str]
    image: Optional[str] = Field(None)
    description: str

    state: InventoryStatus
    updated_at: str
    created_at: str


class User(Document):
    username: str
    hashed_password: str
    inventory: List[Optional[Inventory]] = []


class Admin(Document):
    username: str
    hashed_password: str


# class EquipmentRequest(Document):
#     user_id: str
#     equipment_id: str
#     quantity: int
#     use_purpose: str
#     status: Status

class InventoryApplication(Document):
    user: Link[User]
    inventory: Link[Inventory]
    quantity: int
    use_purpose: str
    status: Status
    
class InventoryPlan(Document):
    name: str
    manufacturer: str
    price: float
    
class InventoryRepair(Document):
    user: Link[User]
    inventory: Link[Inventory]
    description: str
    status: StatusInventoryRepair


class SecretAdmin(Document):
    """
    SecretAdmin model representing an admin user with additional security attributes.

    Attributes:
        hashed_password (str): Hashed password for the admin user.
    """

    hashed_password: str


class AdminFront(Document):
    """
    AdminFront model representing an admin user for the frontend.

    Attributes:
        username (str): Unique username of the admin.
        disabled (bool): Indicates if the admin account is disabled. Default is False.
        full_name (str): Full name of the admin. Default is None.
        secret (Link[SecretAdmin]): Link to the SecretAdmin document containing security details.
    """

    username: str = Field(unique=True)
    disabled: bool = Field(default=False)
    full_name: str = Field(default=None)
    secret: Link[SecretAdmin] = Field()


class Arrow(Document):
    ids: list[int] = []


class Token(BaseModel):
    """
    Token model representing an access token.

    Attributes:
        access_token (str): The access token string.
        token_type (str): The type of the token, typically "bearer".
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData model representing the data contained in a token.

    Attributes:
        username (str): The username associated with the token.
    """

    username: str
