from fastapi import APIRouter, HTTPException, Header
from typing import Dict, Annotated, List
from bson import ObjectId
from app.data import schemas
from app.data.models import InventoryPlan, Admin
from app.routers.user import redis

router = APIRouter(prefix="/inventory_plan", tags=["Inventory Plan"])

@router.post("/")
async def create_inventory_plan(admin_token: Annotated[str, Header()], request: schemas.CreateInventoryPlan) -> schemas.ResponseCreateInventoryPlan:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")
    
    inventory_plan = InventoryPlan(
        name=request.name,
        manufacturer=request.manufacturer,
        price=request.price
    )
    await inventory_plan.create()
    
    return schemas.ResponseCreateInventoryPlan(
        id=str(inventory_plan.id),
        name=inventory_plan.name,
        manufacturer=inventory_plan.manufacturer,
        price=inventory_plan.price
    )


@router.get("/{inventory_plan_id}")
async def get_inventory_plan_by_id(admin_token: Annotated[str, Header()], inventory_plan_id: str) -> schemas.ResponseCreateInventoryPlan:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "User not found")

    inventory_plan = await InventoryPlan.find_one(InventoryPlan.id == ObjectId(inventory_plan_id))
    if not inventory_plan:
        raise HTTPException(404, "Plan not found")

    return schemas.ResponseCreateInventoryPlan(
        id=str(inventory_plan.id),
        name=inventory_plan.name,
        manufacturer=inventory_plan.manufacturer,
        price=inventory_plan.price
    )


@router.get("/all")
async def get_inventory_plan(admin_token: Annotated[str, Header()]) -> List[schemas.ResponseCreateInventoryPlan]:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "User not found")

    inventory_plans = await InventoryPlan.find_all().to_list()
    if not inventory_plans:
        raise HTTPException(404, "Plans not found")

    return [schemas.ResponseCreateInventoryPlan(
        id=str(inventory_plan.id),
        name=inventory_plan.name,
        manufacturer=inventory_plan.manufacturer,
        price=inventory_plan.price
    )
        for inventory_plan in inventory_plans
    ]
    
@router.patch("/status/{inventory_plan_id}")
async def update_inventory_plan(admin_token: Annotated[str, Header()], inventory_plan_id: str, request: schemas.UpdateInventoryPlan) -> schemas.ResponseCreateInventoryPlan:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    admin = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not admin:
        raise HTTPException(404, "Admin not found")
    
    inventory_plan = await InventoryPlan.find_one(InventoryPlan.id == ObjectId(inventory_plan_id))
    if not inventory_plan:
        raise HTTPException(404, "Plan not found")
    
    update_plan = request.model_dump(exclude_unset=True)
    for key, value in update_plan.items():
        setattr(inventory_plan, key, value)
        
    await inventory_plan.save()
        
    return schemas.ResponseCreateInventoryPlan(
        id=str(inventory_plan.id),
        name=inventory_plan.name,
        manufacturer=inventory_plan.manufacturer,
        price=inventory_plan.price
    )

    
@router.delete("/{inventory_plan_id}")
async def delete_inventory_application(admin_token: str, inventory_plan_id: str) -> Dict[str, bool]:
    username = redis.get(admin_token)
    if not username:
        raise HTTPException(401, "Token invalid")

    user = await Admin.find_one(Admin.username == username.decode("utf-8"))
    if not user:
        raise HTTPException(404, "Admin not found")

    inventory_plan = await InventoryPlan.find_one(InventoryPlan.id == ObjectId(inventory_plan_id))
    if not inventory_plan:
        raise HTTPException(404, "Plan not found")

    await inventory_plan.delete()

    return {"status": True}