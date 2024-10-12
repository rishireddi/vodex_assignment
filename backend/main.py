#Third-party Dependencies
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, HTTPException, Depends
from contextlib import asynccontextmanager
from datetime import datetime
from bson import ObjectId
from typing import List

#Local Dependencies
from backend.apis.item_apis import items_router
from backend.apis.clock_in_records_apis import clock_in_records_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client(app)
    yield

    await shutdown_db_client(app)

async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(
       "mongodb+srv://user1:user1@cluster0.x4waj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    app.mongodb = app.mongodb_client.get_database("db_for_assignment")
    app.items_collection = app.mongodb["items"]
    app.clock_in_records_collection = app.mongodb["clock_in_records"]
    print("MongoDB connected.")

async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Hello from Koyeb"}

app.include_router(items_router, prefix="/items", tags=["Items"])
app.include_router(clock_in_records_router, prefix="/clock_in_records", tags=["Clock in Records"])