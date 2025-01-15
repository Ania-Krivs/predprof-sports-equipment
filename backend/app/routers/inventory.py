from fastapi import APIRouter
from app.data.models import Inventory, User
from app.data.schemas import SInventoryId, SInventoryUpdateData, SInventoryAddData
from datetime import datetime
from app.exceptions import InventoryAlreadyExisted

inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])


@inventory_router.delete("/delete_inventory")
async def delete_inventory_by_id(delete_data: SInventoryId) -> dict:
    await (await Inventory.find_one(Inventory.id == delete_data.id)).delete()
    return {"ok": True}


@inventory_router.patch("/update_inventory")
async def update_inventory_by_id(update_data: SInventoryUpdateData) -> dict:
    inventory = await Inventory.find_one(Inventory.id == update_data.id)

    inventory.name = update_data.name
    inventory.amount = update_data.amount
    inventory.state = update_data.state

    if update_data.user_id not in inventory.used_by_user_ids:
        inventory.used_by_user_ids.append(update_data.user_id)

    inventory.updated_at = datetime.now()

    await inventory.save()
    return {"ok": True}


@inventory_router.post("/add_inventory")
async def add_inventory(add_data: SInventoryAddData) -> dict:
    if await Inventory.find_one(add_data.name == Inventory.name):
        raise InventoryAlreadyExisted

    inventory = Inventory(name=add_data.name, amount=add_data.amount, used_by_user_ids=[], state=add_data.state,
                          updated_at=datetime.now(),
                          created_at=datetime.now())

    await inventory.create()
    return {"ok": True}


@inventory_router.get("/all_inventory/")
async def get_all_inventory(filter_by: str = ""):
    return Inventory.find_all(filter_by.lower() in Inventory.name.lower())


@inventory_router.get("/all_user_inventory/{user_id}")
async def get_all_user_inventory(user_id: str):
    inventory = []

    for inventory_id in (await User.find_one(user_id == User.id)).equipment:
        inventory.append(await Inventory.find_one(Inventory.id == inventory_id))

    return inventory


@inventory_router.get("/{inventory_id}")
async def get_inventory_id(inventory_id: str):
    return await Inventory.find_one(inventory_id == Inventory.id)
