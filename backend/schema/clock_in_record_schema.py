#Third-party Dependencies
from datetime import datetime

#Local Dependencies
from backend.models.clock_in_records import ClockInRecordsBase 

class ClockInRecordCreate(ClockInRecordsBase):
    pass

class ClockInRecordsInDatabase(ClockInRecordsBase):
    id          : str
    insert_date : datetime