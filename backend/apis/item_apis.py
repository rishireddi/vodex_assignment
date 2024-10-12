# Third-party Dependencies
from fastapi import APIRouter, HTTPException, Depends, Request
from datetime import datetime
from bson import ObjectId
from typing import List

# Local Dependencies
from backend.schema.item_schema import ItemInDatabase, ItemCreate
from backend.helper.item_helper import item_helper

items_router = APIRouter()

async def get_items_collection(request: Request):
    return request.app.items_collection

@items_router.post("/create", response_model=ItemInDatabase)
async def create_item(item: ItemCreate, items_collection=Depends(get_items_collection)):
    item_data = item.dict()
    item_data["insert_date"] = datetime.now()

    result = await items_collection.insert_one(item_data)
    created_item = await items_collection.find_one({"_id": result.inserted_id})

    if created_item:
        return item_helper(created_item)
    else:
        raise HTTPException(status_code=404, detail="Item could not be created")

@items_router.get("/get_item/{id}", response_model=ItemInDatabase)
async def get_item(id: str, items_collection=Depends(get_items_collection)):
    item = await items_collection.find_one({"_id": ObjectId(id)})
    if item is not None:
        return item_helper(item)
    raise HTTPException(status_code=404, detail="Item not found")

@items_router.get("/filter", response_model=List[ItemInDatabase])
async def filter_items(items_collection=Depends(get_items_collection), email: str = None, expiry_date: datetime = None, insert_date: datetime = None, quantity: int = None):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt": expiry_date}
    if insert_date:
        query["insert_time"] = {"$gt": insert_date}  
    if quantity is not None:
        query["quantity"] = {"$gte": quantity}

    items = await items_collection.find(query).to_list(length=100)
    return [item_helper(item) for item in items]

@items_router.patch("/update/{id}", response_model=ItemInDatabase)
async def update_item(id: str, item: ItemCreate, items_collection=Depends(get_items_collection)):
    update_item_data = {key: value for key, value in item.dict().items() if value is not None}
    result = await items_collection.update_one({"_id": ObjectId(id)}, {"$set": update_item_data})

    if result.modified_count == 1:
        updated_item = await items_collection.find_one({"_id": ObjectId(id)})
        return item_helper(updated_item)
    
    raise HTTPException(status_code=404, detail="Item not found")

@items_router.delete("/delete/{id}")
async def delete_item(id: str, items_collection=Depends(get_items_collection)):
    result = await items_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"detail": "Item deleted"}
    
    raise HTTPException(status_code=404, detail="Item not found")

@items_router.get("/aggregate", response_model=List[dict])
async def aggregate_items(items_collection=Depends(get_items_collection)):
    pipeline = [
        {
            "$group": {
                "_id": "$email",
                "count": {"$sum": 1}
            }
        }
    ]
    result = await items_collection.aggregate(pipeline).to_list(length=100)
    return result
