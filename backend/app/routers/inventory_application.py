from fastapi import APIRouter, HTTPException, Header
from app.data import schemas
from app.data.models import User, InventoryApplication, Inventory
from typing import Optional, Annotated, List, Dict
from app.routers.user import redis
from app.data.models import Status, Admin
from app.exceptions import InventoryNotFound
from bson import ObjectId

router = APIRouter(prefix="/inventory_application", tags=["Inventory Application"])


@router.post("/")
async def create_inventory_application(token: Annotated[str, Header()],
                                       request: schemas.RequestInventoryApplication):
    username = redis.get(token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await User.find_one(User.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "User not found")

    inventory = await Inventory.find_one(InventoryApplication.id == ObjectId(request.inventory_id))
    if not inventory:
        raise InventoryNotFound

    inventory_application = InventoryApplication(
        user=user,
        inventory=inventory.dict(),
        quantity=request.amount,
        use_purpose=request.use_purpose,
        status=Status.AWAITING
    )
    await inventory_application.save()

    return {"_id":str(inventory_application.id),
        "user":user,
        "inventory":inventory,
        "quantity":inventory_application.quantity,
        "use_purpose":inventory_application.use_purpose,
        "status":inventory_application.status
        }
    
@router.get("/id")
async def get_inventory_application_by_id(application_id: str):
    inventory_application = await InventoryApplication.find_one(InventoryApplication.id == ObjectId(application_id), fetch_links=True)
    if not inventory_application:
        raise HTTPException(404, "Application not found")

    return inventory_application

@router.get("/user/{user_token}")
async def get_inventory_application_by_user(user_token: str):
    username = redis.get(user_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await User.find_one(User.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "User not found")

    inventory_applications = await InventoryApplication.find({"user._id": ObjectId(user.id)}, fetch_links=True).to_list()
    if not inventory_applications:
        raise HTTPException(404, "Application not found")

    return [schemas.ResponseGetInventoryApplication(
        _id=str(inventory_application.id),
        user=inventory_application.user,
        inventory=inventory_application.inventory,
        quantity=inventory_application.quantity,
        use_purpose=inventory_application.use_purpose,
        status=inventory_application.status
    )
        for inventory_application in inventory_applications
    ]


@router.get("/all")
async def get_all_inventory_application_with_status(status: Optional[int] = None):
    if status:
        inventory_applications = await InventoryApplication.find(InventoryApplication.status == status, fetch_links=True).to_list()
    else:
        inventory_applications = await InventoryApplication.find(fetch_links=True).to_list()

    if not inventory_applications:
        raise HTTPException(404, "Equipment Applications not found")
    
    return [
        inventory_application for inventory_application in inventory_applications
    ]


@router.patch("/status/{admin_token}")
async def update_status(admin_token: str, request: schemas.RequestApplicationUpdate):
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")
    
    inventory_application = await InventoryApplication.find_one(InventoryApplication.id == ObjectId(request.application_id), fetch_links=True)
    if not inventory_application:
        raise HTTPException(404, "Application not found")

    inventory = await Inventory.find_one(Inventory.id == ObjectId(inventory_application.inventory.id), fetch_links=True)
    if not inventory:
        raise HTTPException(404, detail="Inventory not found")
                            
    inventory_application.status = request.status
    await inventory_application.save()
    
    if int(inventory_application.status) == int(Status.ACCEPTED):
        inventory.amount = (inventory.amount - inventory_application.quantity)
        await inventory.save()
        
        user = await User.find_one(User.id == ObjectId(inventory_application.user.id))
        inventory_ = Inventory(
                _id=inventory.id,
                name=inventory.name,
                amount=inventory.amount,
                used_by_user=inventory.used_by_user,
                image=inventory.image,
                description=inventory.description,
                state=inventory.state,
                updated_at=inventory.updated_at,
                created_at=inventory.created_at
            )
        if user.inventory is None:
            user.inventory = inventory_
        
        else:
            user.inventory.append(inventory_)
        
        await user.save()

    return inventory_application


@router.delete("/{admin_token}")
async def delete_inventory_application(admin_token: str, application_id: Annotated[str, Header()]) -> Dict[str, bool]:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")

    inventory_application = await InventoryApplication.find_one(InventoryApplication.id == ObjectId(application_id))
    if not inventory_application:
        raise HTTPException(404, "Application not found")
    
    user = await User.find_one(Admin.id == ObjectId(inventory_application.user._id), fetch_links=True)
    if not user:
        raise HTTPException(404, "User not found")
    
    lt = []
    for inventory in user.inventory:
        if inventory.id != inventory_application.inventory._id:
            lt.append(inventory)
            
    user.inventory = lt
    await user.save()

    await inventory_application.delete()

    return {"status": True}
