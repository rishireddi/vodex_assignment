# Third-party Dependencies
from fastapi import APIRouter, HTTPException, Depends, Request
from datetime import datetime
from bson import ObjectId
from typing import List

# Local Dependencies
from backend.schema.clock_in_record_schema import ClockInRecordsInDatabase, ClockInRecordCreate
from backend.helper.clock_in_record_helper import clock_in_record_helper

clock_in_records_router = APIRouter()

async def get_clock_in_records_collection(request: Request):
    return request.app.clock_in_records_collection

@clock_in_records_router.post("/create", response_model=ClockInRecordsInDatabase)
async def create_clock_in_records(clock_in_record: ClockInRecordCreate, clock_in_records_collection=Depends(get_clock_in_records_collection)):
    clock_in_record_data = clock_in_record.dict()
    clock_in_record_data["insert_date"] = datetime.now()

    result = await clock_in_records_collection.insert_one(clock_in_record_data)
    created_clock_in_record = await clock_in_records_collection.find_one({"_id": result.inserted_id})

    if created_clock_in_record:
        return clock_in_record_helper(created_clock_in_record)
    else:
        raise HTTPException(status_code=404, detail="Clock In record could not be created")

@clock_in_records_router.get("/get_clock_in_record/{id}", response_model=ClockInRecordsInDatabase)
async def get_clock_in_record(id: str, clock_in_records_collection=Depends(get_clock_in_records_collection)):
    clock_in_record = await clock_in_records_collection.find_one({"_id": ObjectId(id)})
    if clock_in_record is not None:
        return clock_in_record_helper(clock_in_record)
    raise HTTPException(status_code=404, detail="clock_in_record not found")

@clock_in_records_router.get("/filter", response_model=List[ClockInRecordsInDatabase])
async def filter_clock_in_records(clock_in_records_collection=Depends(get_clock_in_records_collection), email: str = None, location: str = None, insert_date: datetime = None):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_date:
        query["insert_time"] = {"$gt": insert_date}  


    clock_in_records = await clock_in_records_collection.find(query).to_list(length=100)
    return [clock_in_record_helper(clock_in_record) for clock_in_record in clock_in_records]

@clock_in_records_router.patch("/update/{id}", response_model=ClockInRecordsInDatabase)
async def update_clock_in_record(id: str, clock_in_record: ClockInRecordCreate, clock_in_records_collection=Depends(get_clock_in_records_collection)):
    update_clock_in_record_data = {key: value for key, value in clock_in_record.dict().items() if value is not None}
    result = await clock_in_records_collection.update_one({"_id": ObjectId(id)}, {"$set": update_clock_in_record_data})

    if result.modified_count == 1:
        updated_clock_in_record = await clock_in_records_collection.find_one({"_id": ObjectId(id)})
        return clock_in_record_helper(updated_clock_in_record)
    
    raise HTTPException(status_code=404, detail="clock_in_record not found")

@clock_in_records_router.delete("/delete/{id}")
async def delete_clock_in_record(id: str, clock_in_records_collection=Depends(get_clock_in_records_collection)):
    result = await clock_in_records_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"detail": "clock_in_record deleted"}
    
    raise HTTPException(status_code=404, detail="clock_in_record not found")
