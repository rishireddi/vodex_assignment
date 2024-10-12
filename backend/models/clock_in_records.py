from pydantic import BaseModel, EmailStr

class ClockInRecordsBase(BaseModel):
    email       : EmailStr
    location    : str