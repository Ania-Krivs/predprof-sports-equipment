from fastapi import APIRouter, HTTPException, Header
from app.data import schemas
from app.data.models import User, InventoryRepair, Inventory, StatusInventoryRepair, InventoryStatus

router = APIRouter(prefix="/statistics", tags=["Statistics"])

@router.get("/")
async def get_statistics() -> schemas.Statistic:
    inventories = await Inventory.find(fetch_links=True).to_list()
    if not inventories:
        raise HTTPException(404, "Inventories not found")
    
    users = await User.find(fetch_links=True).to_list()
    if not users:
        raise HTTPException(404, "Users not found")
    
    inventory_in_use = 0
    for user in users:
        inventory_in_use += len(user.inventory)
        
    inventory_repairs = await InventoryRepair.find(fetch_links=True). to_list()
    if not inventory_repairs:
        raise HTTPException(404, "Inventory repair not found")
    
    inventory_repair_ = 0
    need_to_replace_ = 0
    for inventory_repair in inventory_repairs:
        if inventory_repair.status == StatusInventoryRepair.REPAIR:
            inventory_repair_ += 1
        if inventory_repair.status == StatusInventoryRepair.REPLACING:
            need_to_replace_ += 1
    broken = 0
    for inventory in inventories:
        if inventory.state == InventoryStatus.BROKEN:
            broken += 1
            
    return schemas.Statistic(
        inventory_in_use=inventory_in_use,
        inventory_repair=inventory_repair_,
        need_to_replace=need_to_replace_,
        broken=broken
    )