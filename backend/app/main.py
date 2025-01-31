from beanie import init_beanie, Document, UnionDoc
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

from app import MONGO_DSN, ENVIRONMENT, projectConfig
from app.routers import user, inventory, inventory_application, admin, inventory_plan, inventory_repair, statistics

if ENVIRONMENT == "prod":
    app = FastAPI(
        title=projectConfig.__projname__,
        version=projectConfig.__version__,
        description=projectConfig.__description__,
        docs_url=None
    )

else:
    app = FastAPI(
        title=projectConfig.__projname__,
        version=projectConfig.__version__,
        description=projectConfig.__description__
    )

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(user.router)
app.include_router(inventory.inventory_router)
app.include_router(inventory_application.router)
app.include_router(admin.router)
app.include_router(inventory_plan.router)
app.include_router(inventory_repair.router)
app.include_router(statistics.router)


@app.on_event('startup')
async def startup_event():
    client = AsyncIOMotorClient(MONGO_DSN)

    await init_beanie(
        database=client['Predprof'],
        document_models=Document.__subclasses__() + UnionDoc.__subclasses__()
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
