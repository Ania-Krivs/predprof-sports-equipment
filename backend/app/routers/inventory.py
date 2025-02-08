from fastapi import HTTPException
from typing import Optional, List
from app.data.models import Inventory, User, Admin
from app.data import schemas
from datetime import datetime
from app.exceptions import InventoryAlreadyExisted, InventoryNotFound, UserNotFound, NotEnoughInventory
from fastapi import APIRouter, File, Form, Header
from typing_extensions import Annotated
from app.utils.image import process_image
from app.constants import default_image
from bson import ObjectId
from app.routers.user import redis

import csv

inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])


@inventory_router.delete("/delete_inventory")
async def delete_inventory_by_id(delete_data: schemas.SInventoryId) -> dict:
    inventory = await Inventory.find_one(Inventory.id == ObjectId(delete_data.id))
    if not inventory:
        raise InventoryNotFound

    await inventory.delete()
    return {"ok": True}


@inventory_router.patch("/update_inventory")
async def update_inventory_by_id(update_data: schemas.SInventoryUpdateData) -> dict:
    inventory = await Inventory.find_one(Inventory.id == ObjectId(update_data.id))

    if not inventory:
        raise InventoryNotFound

    inventory.name = update_data.name
    inventory.amount = update_data.amount
    inventory.state = update_data.state
    inventory.description = update_data.description

    if update_data.user_id not in inventory.used_by_user:
        inventory.used_by_user.append(update_data.user_id)

    inventory.updated_at = str(datetime.now())

    await inventory.save()
    return {"_id": str(update_data.id)}


@inventory_router.patch("/update_image")
async def update_image(inventory_id: Annotated[str, Header()], token: Annotated[str, Header()],
                       file: Annotated[bytes, File()],
                       extension: Annotated[str, Form()] = "png") -> dict:
    image = await process_image(file, extension)

    inventory = await Inventory.find_one(Inventory.id == ObjectId(inventory_id))

    if not inventory:
        raise InventoryNotFound

    if token not in inventory.used_by_user:
        inventory.used_by_user.append(token)

    inventory.updated_at = str(datetime.now())

    inventory.image = image["image_link"]
    await inventory.save()

    return {"image_link": image["image_link"], "file_name": f"{image['file_name']}.{extension}",
            "_id": str(inventory.id)}


@inventory_router.post("/add_inventory")
async def add_inventory(add_data: schemas.SInventoryAddData) -> dict:
    if await Inventory.find_one(add_data.name == Inventory.name):
        raise InventoryAlreadyExisted

    inventory = Inventory(name=add_data.name, amount=add_data.amount, used_by_user=[], state=add_data.state,
                          description=add_data.description,
                          image=default_image,
                          updated_at=str(datetime.now()),
                          created_at=str(datetime.now()))

    await inventory.create()
    return {"_id": str((await Inventory.find_one(add_data.name == Inventory.name)).id)}


@inventory_router.post("/add_inventory_to_user/{token}")
async def add_inventory_to_user(token: str, add_data: schemas.SAddInventoryToUser) -> dict:
    username = redis.get(token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")
    user = await User.find_one(User.id == str(add_data.user_id))
    if not user:
        raise HTTPException(404, "User not found")
    
    inventory = await Inventory.find_one(Inventory.id == ObjectId(add_data.inventory_id))

    if not inventory:
        raise InventoryNotFound

    if inventory.amount < add_data.amount:
        raise NotEnoughInventory

    user.inventory.append(inventory)

    return {"user_id": str(user.id), "_id": str(inventory.id)}


@inventory_router.get("/all_inventory/")
async def get_all_inventory(filter_by: Optional[str] = None):

    if filter_by:
        inventories = await Inventory.find({"name": filter_by}).to_list()
    else:
        inventories = await Inventory.find_all().to_list()

    return [inventory for inventory in inventories]


@inventory_router.get("/all_user_inventory/{token}")
async def get_all_user_inventory(token: str):
    username = redis.get(token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await User.find_one(User.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "User not found")

    inventories = []

    for inventory_id in user.inventory:
        inventory = await Inventory.find_one(Inventory.id == inventory_id)
        if inventory:
            inventories.append(inventory)

    return inventories


@inventory_router.get("/{inventory_id}")
async def get_inventory_id(inventory_id: str):
    inventory = await Inventory.find_one(ObjectId(inventory_id) == Inventory.id)
    if not inventory:
        raise HTTPException(404, "Inventory not found")
    
    return inventory


@inventory_router.get("/export_table/")
async def get_table_inventorys():
    all_data = await User.find_all().to_list()
    with open('output.csv', 'w', newline='') as f:
        csv.DictWriter(f).writerows(all_data)
    with open('output.csv', 'r', newline='') as f:
        pass
    return ''