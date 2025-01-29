from fastapi import APIRouter, HTTPException
from typing import Dict
from bson import ObjectId
from app.data import schemas
from app.data.models import User, Admin, Inventory
from app.utils.auth import create_admin, authenticate_user
from app.utils.security import verify_password
from app.routers.user import redis
from app import ACCESS_TOKEN_EXPIRE_MINUTES_REDIS

router = APIRouter(prefix="/admin", tags=["Admin"])


# @router.post("/create")
# async def registration_admin(request: schemas.RequestCreateUser) -> schemas.ResponseUserLogIn:
#     user = await create_admin(request)
#     token = await authenticate_user(data={"sub": request.username})
    
#     redis.set(token, user.username, ex=int(ACCESS_TOKEN_EXPIRE_MINUTES_REDIS))

#     return schemas.ResponseUserLogIn(
#         user_token=token
#     )


@router.post("/log_in")
async def log_in_admin(request: schemas.RequestLogInUser) -> schemas.ResponseAdminLogIn:
    admin = await Admin.find_one(User.username == request.username)
    if not admin or not verify_password(request.password, admin.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect name or password")

    token = await authenticate_user(data={"sub": request.username})

    redis.set(token, admin.username, ex=int(ACCESS_TOKEN_EXPIRE_MINUTES_REDIS))

    return schemas.ResponseAdminLogIn(
        admin_token=token
    )
    
@router.patch("/assignment_inventory/{admin_token}")
async def assignment_inventory_by_user(admin_token: str, request: schemas.RequestAssignmentInventory) -> Dict[str, bool]:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")
    
    user = await User.find_one(User.id == ObjectId(request.user_id), fetch_links=True)
    if not user:
        raise HTTPException(404, "User not found")
    
    inventory = await Inventory.find_one(Inventory.id == ObjectId(request.inventory_id), fetch_links=True)
    if not inventory:
        raise HTTPException(404, detail="Inventory not found")
    
    inventory_ = Inventory(
                id=inventory.id,
                name=inventory.name,
                amount=inventory.amount,
                used_by_user=inventory.used_by_user,
                image=inventory.image,
                description=inventory.description,
                state=inventory.state,
                updated_at=inventory.updated_at,
                created_at=inventory.created_at
            )
    
    user.inventory.append(inventory_)
    
    await user.save()
    
    return {"status": True}


