from app.data.models import Inventory, User
from app.data import schemas
from datetime import datetime
from app.exceptions import InventoryAlreadyExisted
from fastapi import APIRouter, File, Form
from typing_extensions import Annotated
from app.utils.image import process_image
from app.constants import default_image

inventory_router = APIRouter(prefix="/inventory", tags=["Inventory"])


@inventory_router.delete("/delete_inventory")
async def delete_inventory_by_id(delete_data: schemas.SInventoryId) -> dict:
    await (await Inventory.find_one(Inventory.id == delete_data.id)).delete()
    return {"ok": True}


@inventory_router.patch("/update_inventory")
async def update_inventory_by_id(update_data: schemas.SInventoryUpdateData) -> dict:
    inventory = await Inventory.find_one(Inventory.id == update_data.id)

    inventory.name = update_data.name
    inventory.amount = update_data.amount
    inventory.state = update_data.state
    inventory.description = update_data.description

    if update_data.user_id not in inventory.used_by_user_ids:
        inventory.used_by_user_ids.append(update_data.user_id)

    inventory.updated_at = datetime.now()

    await inventory.save()
    return {"ok": True, "id": update_data.id}


@inventory_router.patch("/update_inventory_image")
async def update_inventory_image(inventory_data: schemas.SInventoryUpdateImage, file: Annotated[bytes, File()],
                                 extension: Annotated[str, Form()] = "png") -> dict:
    image = await process_image(file, extension)

    inventory = await Inventory.find_one(Inventory.id == inventory_data.id)
    
    if inventory_data.user_id not in inventory.used_by_user_ids:
        inventory.used_by_user_ids.append(inventory_data.user_id)

    inventory.updated_at = datetime.now()

    inventory.image = image["image_link"]
    await inventory.save()

    return {"ok": True, "image_link": image["image_link"], "file_name": f"{image['file_name']}.{extension}",
            "id": inventory.id}


@inventory_router.post("/add_inventory")
async def add_inventory(add_data: schemas.SInventoryAddData, file: Annotated[bytes, File(), None] = None,
                        extension: Annotated[str, Form()] = "png") -> dict:
    if await Inventory.find_one(add_data.name == Inventory.name):
        raise InventoryAlreadyExisted

    if not file:
        image = default_image
    else:
        image = (await process_image(file, extension))["image_link"]

    inventory = Inventory(name=add_data.name, amount=add_data.amount, used_by_user_ids=[], state=add_data.state,
                          descriprion=add_data.description,
                          image=image,
                          updated_at=datetime.now(),
                          created_at=datetime.now())

    await inventory.create()
    return {"ok": True, "id": (await Inventory.find_one(add_data.name == Inventory.name)).id}


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
