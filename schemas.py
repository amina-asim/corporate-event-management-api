from datetime import date
from typing import Optional
#from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, ConfigDict
class EventCreate(BaseModel):

    title: str = Field(..., min_length=1, max_length=200)

    description: Optional[str] = None

    event_date: date

    location: str = Field(..., min_length=1, max_length=200)

    max_capacity: int = Field(..., gt=0)
class EventUpdate(BaseModel):
    
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)

    description: Optional[str] = None

    event_date: Optional[date] = None

    location: Optional[str] = Field(default=None, min_length=1, max_length=200)

    max_capacity: Optional[int] = Field(default=None, gt=0)
class EventResponse(BaseModel):
    
    id: int
    title: str
    description: Optional[str]
    event_date: date
    location: str
    max_capacity: int

    model_config = ConfigDict(from_attributes=True)

class RegistrationCreate(BaseModel):
    employee_name: str = Field(..., min_length=1, max_length=100)

    employee_email: str = Field(..., min_length=1, max_length=150)


class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    employee_name: str
    employee_email: str

    model_config = ConfigDict(from_attributes=True)