from fastapi import HTTPException
from typing import Optional, List
from app.data.models import Inventory
from app.data import schemas
from datetime import datetime
from app.exceptions import InventoryAlreadyExisted, InventoryNotFound, UserNotFound, NotEnoughInventory
from fastapi import APIRouter, File, Form, Header
from typing_extensions import Annotated
from app.utils.image import process_image
from app.constants import default_image
from bson import ObjectId
from app.routers.user import redis


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
    return {"id": str(update_data.id)}


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
            "id": str(inventory.id)}


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
    return {"id": str((await Inventory.find_one(add_data.name == Inventory.name)).id)}


@inventory_router.post("/add_inventory_to_user")
async def add_inventory_to_user(add_data: schemas.SAddInventoryToUser) -> dict:
    user = redis.get(add_data.user_id)

    if not user:
        raise UserNotFound

    inventory = await Inventory.find_one(Inventory.id == ObjectId(add_data.id))

    if not inventory:
        raise InventoryNotFound

    if inventory.amount < add_data.amount:
        raise NotEnoughInventory

    user.equipment.append(inventory)

    return {"user_id": str(user.id), "id": str(inventory.id)}


@inventory_router.get("/all_inventory/")
async def get_all_inventory(filter_by: Optional[str] = None) -> List[schemas.RequestInventory]:

    if filter_by:
        inventories = await Inventory.find({"name": filter_by}).to_list()
    else:
        inventories = await Inventory.find_all().to_list()

    return [schemas.RequestInventory(
        id=str(inventory.id),
        name=inventory.name,
        amount=inventory.amount,
        used_by_user=inventory.used_by_user,
        image=inventory.image,
        description=inventory.description,
        state=inventory.state,
        updated_at=inventory.updated_at,
        created_at=inventory.created_at
    )
       for inventory in inventories     
    ]


@inventory_router.get("/all_user_inventory/{user_id}")
async def get_all_user_inventory(user_id: str) -> schemas.RequestInventory:
    user = redis.get(user_id)

    if not user:
        raise UserNotFound

    inventory = []

    for inventory_id in user.equipment:
        inventory.append(await Inventory.find_one(Inventory.id == inventory_id))

    return schemas.RequestInventory(
        id=str(inventory.id),
        name=inventory.name,
        amount=inventory.amount,
        used_by_user=inventory.used_by_user,
        image=inventory.image,
        description=inventory.description,
        state=inventory.state,
        updated_at=inventory.updated_at,
        created_at=inventory.created_at
    )


@inventory_router.get("/{inventory_id}")
async def get_inventory_id(inventory_id: str) -> schemas.RequestInventory:
    inventory = await Inventory.find_one(ObjectId(inventory_id) == Inventory.id)
    if not inventory:
        raise HTTPException(404, "Inventory not found")
    
    return schemas.RequestInventory(
        id=str(inventory.id),
        name=inventory.name,
        amount=inventory.amount,
        used_by_user=inventory.used_by_user,
        image=inventory.image,
        description=inventory.description,
        state=inventory.state,
        updated_at=inventory.updated_at,
        created_at=inventory.created_at
    )
