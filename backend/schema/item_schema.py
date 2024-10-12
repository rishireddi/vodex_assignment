#Third-party Dependencies
from datetime import datetime

#Local Dependencies
from backend.models.items import ItemBase

class ItemCreate(ItemBase):
    pass

class ItemInDatabase(ItemBase):
    id          : str
    insert_date : datetime