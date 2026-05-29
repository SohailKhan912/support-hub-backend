from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Note schemas
class NoteBase(BaseModel):
    note_text: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    ticket_id: str
    created_at: datetime

    class Config:
        from_attributes = True

# Ticket schemas
class TicketBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    subject: str
    description: str

class TicketCreate(TicketBase):
    pass

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    new_note: Optional[str] = None

class Ticket(TicketBase):
    id: int
    ticket_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    notes: List[Note] = []

    class Config:
        from_attributes = True
