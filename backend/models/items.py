#Third-party Dependencies
from pydantic import BaseModel, EmailStr
from datetime import datetime

class ItemBase(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: datetime