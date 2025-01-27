from fastapi import APIRouter, HTTPException, Header
from app.data import schemas
from app.data.models import User, InventoryApplication, Inventory
from typing import Optional, Annotated, List
from app.routers.user import redis
from app.data.models import Status, Admin
from app.exceptions import InventoryNotFound
from bson import ObjectId

router = APIRouter(prefix="/inventory_application", tags=["Inventory Application"])


@router.post("/create")
async def create_inventory_application(token: Annotated[str, Header()],
                                       request: schemas.RequestInventoryApplication) \
        -> schemas.ResponseInventoryApplication:
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

    return schemas.ResponseInventoryApplication(
        user_id=str(user.id),
        inventory=inventory,
        quantity=inventory_application.quantity,
        use_purpose=inventory_application.use_purpose,
        status=inventory_application.status
    )


@router.get("/get/{user_token}")
async def get_inventory_application_by_user(user_token: str) -> list[schemas.ResponseGetInventoryApplication]:
    username = redis.get(user_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await User.find_one(User.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "User not found")

    inventory_applications = await InventoryApplication.find(
        InventoryApplication.user_id == ObjectId(user.id)).to_list()
    if not inventory_applications:
        raise HTTPException(404, "Application not found")

    return [schemas.ResponseGetInventoryApplication(
        user_id=inventory_application.user_id,
        equipment_id=inventory_application.equipment_id,
        quantity=inventory_application.quantity,
        use_purpose=inventory_application.use_purpose,
        status=inventory_application.status
    )
        for inventory_application in inventory_applications
    ]


@router.get("/get_all")
async def get_all_inventory_application_with_status(status: Optional[int] = None) \
        -> List[schemas.ResponseGetInventoryApplication]:
    if status:
        inventory_applications = await InventoryApplication.find(InventoryApplication.status == status).to_list()
    else:
        inventory_applications = await InventoryApplication.find_all().to_list()

    if not inventory_applications:
        raise HTTPException(404, "Equipment Applications not found")

    return [schemas.ResponseGetInventoryApplication(
        user_id=inventory_application.user_id,
        inventory=str(inventory_application.inventory.id),
        quantity=inventory_application.quantity,
        use_purpose=inventory_application.use_purpose,
        status=inventory_application.status
    )
        for inventory_application in inventory_applications
    ]


@router.patch("/update_status/{admin_token}")
async def update_status(admin_token: str, request: schemas.RequestApplicationUpdate):
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "Admin not found")

    inventory_application = await InventoryApplication.find_one(
        InventoryApplication.id == ObjectId(request.application_id))
    if not inventory_application:
        raise HTTPException(404, "Application not found")

    inventory_application.status = request.status
    await inventory_application.save()

    return "ok"


@router.delete("/delete/{admin_token}")
async def delete_inventory_application(admin_token: str, application_id: Annotated[str, Header()]):
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "Admin not found")

    inventory_application = await InventoryApplication.find_one(InventoryApplication.id == ObjectId(application_id))
    if not inventory_application:
        raise HTTPException(404, "Application not found")

    await inventory_application.delete()

    return "ok"
