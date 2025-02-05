from fastapi import APIRouter, HTTPException, Header
from app.data import schemas
from app.data.models import User, InventoryApplication, Inventory, InventoryRepair, StatusInventoryRepair
from typing import Optional, Annotated, List, Dict
from app.routers.user import redis
from app.data.models import Status, Admin
from app.exceptions import InventoryNotFound
from bson import ObjectId

router = APIRouter(prefix="/inventory_repair", tags=["Inventory Repair"])

@router.post("/")
async def create_application_for_inventory_repair(token: Annotated[str, Header()],
                                       request: schemas.RequestInventoryRepair):
    username = redis.get(token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await User.find_one(User.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "User not found")

    inventory = await Inventory.find_one(InventoryApplication.id == ObjectId(request.inventory_id))
    if not inventory:
        raise InventoryNotFound

    inventory_repair = InventoryRepair(
        user=user,
        inventory=inventory,
        description=request.description,
        status=request.status
    )
    await inventory_repair.save()

    return {"_id":str(inventory_repair.id),
        "user":user,
        "inventory":inventory,
        "description":inventory_repair.description,
        "status":inventory_repair.status
        }
    
@router.get("/{admin_token}")
async def get_application_for_inventory_repair(admin_token: str, application_id: str):
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")
    
    inventory_repair = await InventoryRepair.find_one(InventoryRepair.id == ObjectId(application_id), fetch_links=True)
    if not inventory_repair:
        raise HTTPException(404, "Application not found")

    return inventory_repair
    
@router.get("/all/{admin_token}")
async def get_application_for_inventory_repair(admin_token: str) -> List:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")
    
    inventory_repairs = await InventoryRepair.find(fetch_links=True).to_list()
    if not inventory_repairs:
        raise HTTPException(404, "Applications not found")

    return [
       inventory_repair for inventory_repair in inventory_repairs
    ]
    
@router.delete("/{admin_token}")
async def delete_application_for_inventory_repair(admin_token: str, application_id: Annotated[str, Header()]) -> Dict[str, bool]:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")

    inventory_repair = await InventoryRepair.find_one(InventoryRepair.id == ObjectId(application_id), fetch_links=True)
    if not inventory_repair:
        raise HTTPException(404, "Application not found")

    await inventory_repair.delete()

    return {"status": True}